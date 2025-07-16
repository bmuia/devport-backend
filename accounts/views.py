from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from django.shortcuts import redirect
from urllib.parse import urlencode

from .serializers import RegistrationSerializer
from .social_providers import (
    get_google_auth_url,
    get_google_tokens,
    get_google_user_info
)

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "email": user.email},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        url = get_google_auth_url()
        return redirect(url)


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return Response({"error": "Missing authorization code"}, status=400)

        token_response = get_google_tokens(code)
        access_token = token_response.get("access_token")

        if not access_token:
            return Response({"error": "Failed to get access token"}, status=400)

        user_info = get_google_user_info(access_token)

        email = user_info.get("email")
        name = user_info.get("name", "")

        if not email:
            return Response({"error": "Email not found in Google response"}, status=400)

        user, _ = User.objects.update_or_create(
            email=email
        )

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        # Redirect to frontend with tokens in URL
        query_params = urlencode({
            "access": str(access),
            "refresh": str(refresh),
            "email": email,
            "name": name
        })
        return redirect(f"http://localhost:3000/oauth/callback?{query_params}")
