

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from rbac.views import (

    # authentication classes
    RegisterClassView,
    
    # File Management
    FileDetailView,
    FileListCreateView,
    
    # Permission Management
    FileEditorsView,
    FileViewersView
)



urlpatterns = [
    # Unit Tests Done Of Authentication Views
    path("auth/register/", RegisterClassView.as_view(),name="register_view"),
    path("auth/login/", TokenObtainPairView.as_view(),name="login_view"),
    path("auth/logout/", TokenBlacklistView.as_view(),name="logout_view"),
    path("auth/token/refresh/", TokenRefreshView.as_view(),name="refresh_token_view"),
    
    
    # Unit Tests Done for Get and Create
    path("file/",FileListCreateView.as_view(), name="File-create"),
    
    # Unit Tests Done For Get Put Patch Delete 
    path("file/<int:pk>/",FileDetailView.as_view(), name="File"),
    
    # File Permissions Unit Tests Done
    path("file/<int:pk>/editors/", FileEditorsView.as_view(), name="file-editors"),
    path("file/<int:pk>/viewers/", FileViewersView.as_view(), name="file-viewers")
    
    
    
]
