from rest_framework.permissions import BasePermission


import logging
from rest_framework.permissions import BasePermission
from rest_framework import status

logger = logging.getLogger(__name__)

class FilePermission(BasePermission):
    """
    Comprehensive permission class for File model with advanced access control.
    
    Permission Levels:
    - Owner: Full access (read, write, delete)
    - Editors: Read and write
    - Viewers: Read-only
    """
    
    def has_permission(self, request, view):
        """
        Global permission check before object-level permissions.
        
        Prevents unauthorized users from accessing any file-related views.
        """
        # Authenticated users only
        if not request.user or not request.user.is_authenticated:
            logger.warning(f"Unauthorized access attempt: {request.method}")
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Granular object-level permission checks.
        
        Args:
            request: Current HTTP request
            view: Current view
            obj: File object being accessed
        
        Returns:
            bool: Permission granted or denied
        """
        try:
            # Superuser always has full access
            if request.user.is_superuser:
                return True
            
            # Safe methods (read-only)
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return self._check_read_permission(request, obj)
            
            # Modification methods
            if request.method in ['POST', 'PUT', 'PATCH']:
                return self._check_write_permission(request, obj)
            
            # Deletion method
            if request.method == 'DELETE':
                return self._check_delete_permission(request, obj)
            
            # Unknown method
            logger.warning(f"Unhandled HTTP method: {request.method}")
            return False
        
        except Exception as e:
            logger.error(f"Permission check error: {str(e)}")
            return False
    
    def _check_read_permission(self, request, obj):
        """
        Check read permissions with detailed logging.
        
        Args:
            request: Current HTTP request
            obj: File object
        
        Returns:
            bool: Read permission granted
        """
        is_allowed = (
            request.user == obj.owner or 
            request.user in obj.viewers.all() or 
            request.user in obj.editors.all()
        )
        
        if not is_allowed:
            logger.warning(
                f"Read access denied for user {request.user.username} "
                f"to file {obj.id}"
            )
        
        return is_allowed

    def _check_write_permission(self, request, obj):
        is_allowed = (
            request.user == obj.owner or 
            request.user in obj.editors.all()
        )
        
        if not is_allowed:
            logger.warning(
                f"Write access denied for user {request.user.username} "
                f"to file {obj.id}"
            )
        
        return is_allowed
    
    def _check_delete_permission(self, request, obj):
        """
        Check delete permissions with detailed logging.
        
        Args:
            request: Current HTTP request
            obj: File object
        
        Returns:
            bool: Delete permission granted
        """
        is_allowed = request.user == obj.owner
        print(f"is allowed {is_allowed}")
        if not is_allowed:
            logger.warning(
                f"Delete access denied for user {request.user.username} "
                f"to file {obj.id}"
            )
        
        return is_allowed