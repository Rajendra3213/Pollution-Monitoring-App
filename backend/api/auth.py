from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken

def get_user_id_from_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        return user_id
    except Exception as e:
        print(f"Error decoding access token: {e}")
        return None

class CustomHttpBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            authentication = JWTAuthentication()
            validated_token = authentication.get_validated_token(token)
            user = authentication.get_user(validated_token)
            return user, validated_token
        except InvalidToken:
            return None
        
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "msg":"sucessful login",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }