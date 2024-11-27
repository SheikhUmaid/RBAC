from django.db import models
from django.contrib.auth.models import User






class File(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='owned_files', on_delete=models.CASCADE)
    editors = models.ManyToManyField(User, related_name='editable_files', blank=True)
    viewers = models.ManyToManyField(User, related_name='viewable_files', blank=True)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.name

