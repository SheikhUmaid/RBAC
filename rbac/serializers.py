from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator
from rbac.models import File





class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'content', 'owner']
        read_only_fields = ['owner']

    def validate_editors(self, value):
        """
        Custom validation for editors
        - Prevent duplicate entries
        - Ensure users exist
        """
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate editors are not allowed")
        return value

    def validate_viewers(self, value):
        """
        Custom validation for viewers
        - Prevent duplicate entries
        - Ensure users exist
        """
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate viewers are not allowed")
        return value


class FileDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['id', 'name', 'content', 'owner']

    def get_owner(self, obj):
        """
        Custom method to get owner details
        Allows more flexible owner representation
        """
        return {
            'id': obj.owner.id,
            'username': obj.owner.username,
            'email': obj.owner.email
        }

    def get_editors(self, obj):
        """
        Custom method to get editors
        - Provides more control
        - Allows additional filtering or permissions
        """
        return [
            {
                'id': editor.id,
                'username': editor.username
            } for editor in obj.editors.all()
        ]

    def get_viewers(self, obj):
        """
        Custom method to get viewers
        - Provides more control
        - Allows additional filtering or permissions
        """
        return [
            {
                'id': viewer.id,
                'username': viewer.username
            } for viewer in obj.viewers.all()
        ]








    def validate(self, data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Request user is not available")
        
        owner = request.user
        # Validate editors
        if 'editors' in data and owner in data['editors']:
            raise serializers.ValidationError("Owner cannot be an editor")
        
        # Validate viewers
        if 'viewers' in data and owner in data['viewers']:
            raise serializers.ValidationError("Owner cannot be a viewer")
        
        return data


class FilePermissionSerializer(serializers.ModelSerializer):
    editors = serializers.SlugRelatedField(
        many=True, slug_field='username', queryset=User.objects.all()
    )
    viewers = serializers.SlugRelatedField(
        many=True, slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = File
        fields = ['editors', 'viewers']


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        min_length=3,
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username must be alphanumeric'
            )
        ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator()]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=8,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                message='Password must include letters, numbers, and special characters'
            )
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
        except Exception as e:
            raise serializers.ValidationError(f"User creation failed: {str(e)}")