from django.urls import path
from .views import RegistrationView,LogoutView, GoogleCallbackView,GoogleLoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register-user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view(), name="logout-user"),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('auth/google/callback/', GoogleCallbackView.as_view(), name='google-callback'),
]
