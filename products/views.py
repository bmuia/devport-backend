from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import App, AccessToken
from django.utils import timezone
from datetime import timedelta
import base64
import secrets
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta


class CreateAppView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        title = request.data.get("title")




        app = App.objects.create(
            title=title,
            client=request.user
        )

        return Response({
            'title': app.title,
            'consumer_key': app.consumer_key,
            'consumer_secret': app.consumer_secret,
            'created_at': app.created_at
        }, status=status.HTTP_200_OK)
        

        

class GenerateToken(APIView):
    authentication_classes = []  

    def post(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Basic "):
            return Response({"error": "Missing or invalid Authorization header"}, status=401)

        try:
            # Decode the base64 credentials
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode()
            consumer_key, consumer_secret = decoded_credentials.split(":")
        except Exception:
            return Response({"error": "Invalid Basic Auth format"}, status=400)

        try:
            app = App.objects.get(consumer_key=consumer_key, consumer_secret=consumer_secret)
        except App.DoesNotExist:
            return Response({"error": "Invalid consumer credentials"}, status=401)

        # Generate and save access token
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=1)
        expires_in_seconds = int((expires_at - timezone.now()).total_seconds())


        AccessToken.objects.filter(product=app).update(revoked=True)

        access_token = AccessToken.objects.create(
            product=app,
            token=token,
            expires_at=expires_at
        )

        return Response({
            "access_token": access_token.token,
            "expires_at": expires_in_seconds,
            "token_type": "Bearer"
        }, status=200)
    

