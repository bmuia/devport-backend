from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import base64
import secrets

from .models import App, AccessToken
from .serializers import AppSerializer,AccessTokenSerializer

class AppListView(generics.ListAPIView):
    queryset = App.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AppSerializer


class AppCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get("title")

        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

        app = App.objects.create(
            title=title,
            client=request.user
        )

        return Response({
            'title': app.title,
            'consumer_key': app.consumer_key,
            'consumer_secret': app.consumer_secret,
            'created_at': app.created_at
        }, status=status.HTTP_201_CREATED)
    
class AccessTokenListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccessTokenSerializer

    def get_queryset(self):

        return AccessToken.objects.filter(product__client=self.request.user).order_by('-created_at')

class AccessTokenGenerateView(APIView):
    authentication_classes = []  

    def post(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Basic "):
            return Response({"error": "Missing or invalid Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode()
            consumer_key, consumer_secret = decoded_credentials.split(":")
        except Exception:
            return Response({"error": "Invalid Basic Auth format"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            app = App.objects.get(consumer_key=consumer_key, consumer_secret=consumer_secret)
        except App.DoesNotExist:
            return Response({"error": "Invalid consumer credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Revoke existing tokens
        AccessToken.objects.filter(product=app).update(revoked=True)

        # Create new access token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=1)
        expires_in = int((expires_at - timezone.now()).total_seconds())

        access_token = AccessToken.objects.create(
            product=app,
            token=token,
            expires_at=expires_at
        )

        return Response({
            "access_token": access_token.token,
            "expires_at": expires_in,
            "token_type": "Bearer"
        }, status=status.HTTP_200_OK)
