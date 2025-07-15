from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AccessToken


class JWTProductAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header  or not auth_header.startswith('Bearer '):
            return None
        
        token_key = auth_header.split(" ")[1]


            
        try:
                token = AccessToken.objects.get(token=token_key)
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed("Invalid token. No such token found.")
            
        if token.is_expired():
            raise AuthenticationFailed("Token has expired.")
        
        return (token.product.client, token)
        

        