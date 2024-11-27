from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rbac.serializers import RegisterSerializer, FileDetailSerializer, FileSerializer
from rbac.models import File
from rbac.permissions import FilePermission
import logging




# Authentication Class Views



logger = logging.getLogger(__name__)

class RegisterClassView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]  # Prevent brute force

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            
            # Validate data before save
            if not serializer.is_valid():
                # Log validation errors
                logger.warning(f"Registration validation failed: {serializer.errors}")
                return Response({
                    "message": "Registration failed",
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Save and get the created user
            user = serializer.save()
            
            # Log successful registration
            logger.info(f"User registered: {user.username}")
            
            return Response({
                "message": "User registered successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            # Catch and log any additional validation errors
            logger.error(f"Validation error during registration: {str(e)}")
            return Response({
                "message": "Registration failed",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Catch and log unexpected errors
            logger.critical(f"Unexpected error during registration: {str(e)}")
            return Response({
                "message": "An unexpected error occurred",
                "errors": "Internal server error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': self.page.paginator.num_pages,
            'total_items': self.page.paginator.count,
            'results': data
        })


class FileListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve files with advanced querying and caching
        """
        try:
            files = File.objects.filter(
                Q(owner=request.user) |  
                Q(editors=request.user) | 
                Q(viewers=request.user)
            ).select_related('owner').prefetch_related('editors', 'viewers').distinct()
            # Pagination
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 10)


            paginator = CustomPagination()
            paginated_files = paginator.paginate_queryset(files, request)
            serializer = FileDetailSerializer(paginated_files, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            logger.error(f"Error retrieving files: {str(e)}")
            return Response(
                {"error": "Unable to retrieve files"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        Create a new file with advanced validation and logging
        """
        try:
            # Use detailed serializer for creation
            serializer = FileSerializer(data=request.data)
            
            # Comprehensive validation
            if not serializer.is_valid():
                logger.warning(f"File creation failed: {serializer.errors}")
                return Response(
                    {"errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Custom save with additional context
            file_obj = serializer.save(owner=request.user)
            
            # Log file creation
            logger.info(f"File created: {file_obj.id} by user {request.user.username}")
            
            # Clear user's file cache
            # cache.delete(f'user_files_{request.user.id}')
            
            return Response(
                FileSerializer(file_obj).data, 
                status=status.HTTP_201_CREATED
            )
        
        except ValidationError as ve:
            logger.error(f"Validation error during file creation: {str(ve)}")
            return Response(
                {"error": str(ve)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            print(e)
            logger.critical(f"Unexpected error during file creation: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FileDetailView(APIView):
    permission_classes = [IsAuthenticated, FilePermission]

    def _get_file(self, pk, request):
        """
        Centralized method to retrieve and check permissions for a file
        
        Args:
            pk (int): Primary key of the file
            request (Request): Django REST Framework request object
        
        Returns:
            File: File object with permissions checked
        
        Raises:
            PermissionDenied: If user lacks permissions
            Http404: If file not found
        """
        try:
            file = get_object_or_404(File, pk=pk)
            self.check_object_permissions(request, file)
            return file
        except Exception as e:
            logger.error(f"File retrieval error: {str(e)}")
            raise

    def get(self, request, pk):
        """
        Retrieve file details with comprehensive error handling
        """
        try:
            file = self._get_file(pk, request)
            
            # Use serializer for consistent response
            serializer = FileDetailSerializer(file)
            
            logger.info(f"File retrieved: {pk} by user {request.user.username}")
            return Response(serializer.data)
        
        except Exception as e:
            logger.error(f"Get file error: {str(e)}")
            return Response(
                {"error": f"{str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        """
        Complete file update with comprehensive validation
        """
        try:
            file = self._get_file(pk, request)
            
            # Use serializer for validation
            serializer = FileDetailSerializer(
                file, 
                data=request.data, 
                partial=False
            )
            
            if serializer.is_valid():
                serializer.save()
                
                logger.info(f"File updated: {pk} by user {request.user.username}")
                return Response(serializer.data)
            
            logger.warning(f"File update validation failed: {serializer.errors}")
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValidationError as ve:
            logger.error(f"Validation error during file update: {str(ve)}")
            return Response(
                {"error": str(ve)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.critical(f"Unexpected error during file update: {str(e)}")
            return Response(
                {"error": f"{str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        """
        Partial file update with comprehensive validation
        """
        try:
            file = self._get_file(pk, request)
            
            # Use serializer for validation
            serializer = FileDetailSerializer(
                file, 
                data=request.data, 
                context = {'request':request},
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                
                # logger.info(f"File partially updated: {pk} by user {request.user.username}")
                return Response(serializer.data)
            
            logger.warning(f"Partial file update validation failed: {serializer.errors}")
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ValidationError as ve:
            logger.error(f"Validation error during partial file update: {str(ve)}")
            return Response(
                {"error": str(ve)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.critical(f"Unexpected error during partial file update: {str(e)}")
            print(e)
            return Response(
                {"error": f"{str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        """
        File deletion with comprehensive logging and error handling
        """
        try:
            file = self._get_file(pk, request)
            
            # Optional: Soft delete instead of hard delete
            file.is_deleted = True
            file.save()
            
            logger.info(f"File deleted: {pk} by user {request.user.username}")
            return Response(
                {"message": "File marked as deleted"},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.critical(f"Deletion error: {str(e)}")
            print(e)
            return Response(
                {"error": f"{str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FileEditorsView(APIView):
    permission_classes = [IsAuthenticated, FilePermission]

    def post(self, request, pk):
        """
        Add a user to the file's editors.
        """
        file = get_object_or_404(File, pk=pk)
        self.check_object_permissions(request, file)  # Only owner can modify permissions
        
        
        if request.user != file.owner:
            return Response({"detail": "you dont have have permission for this action"}, status=403)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "User ID is required"}, status=400)

        try:
            user = get_user_model().objects.get(pk=user_id)
            file.editors.add(user)
            return Response({"detail": f"User {user.username} added as an editor."})
        except get_user_model().DoesNotExist as e:
            return Response({"detail": f"User not founds {e}" }, status=404)

    def delete(self, request, pk):
        """
        Remove a user from the file's editors.
        """
        file = get_object_or_404(File, pk=pk)
        self.check_object_permissions(request, file)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "User ID is required"}, status=400)

        try:
            user = get_user_model().objects.get(pk=user_id)
            file.editors.remove(user)
            return Response({"detail": f"User {user.username} removed from editors."})
        except get_user_model().DoesNotExist:
            return Response({"detail": "User not found"}, status=404)
        
        
class FileViewersView(APIView):
    permission_classes = [IsAuthenticated, FilePermission]

    def post(self, request, pk):
        """
        Add a user to the file's editors.
        """
        file = get_object_or_404(File, pk=pk)
        self.check_object_permissions(request, file)  # Only owner can modify permissions
        
        
        if request.user != file.owner:
            return Response({"detail": "you dont have have permission for this action"}, status=403)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "User ID is required"}, status=400)

        try:
            user = get_user_model().objects.get(pk=user_id)
            file.viewers.add(user)
            return Response({"detail": f"User {user.username} added as an editor."})
        except get_user_model().DoesNotExist as e:
            return Response({"detail": f"User not founds {e}" }, status=404)

    def delete(self, request, pk):
        """
        Remove a user from the file's editors.
        """
        file = get_object_or_404(File, pk=pk)
        self.check_object_permissions(request, file)

        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "User ID is required"}, status=400)

        try:
            user = get_user_model().objects.get(pk=user_id)
            file.viewers.remove(user)
            return Response({"detail": f"User {user.username} removed from editors."})
        except get_user_model().DoesNotExist:
            return Response({"detail": "User not found"}, status=404)