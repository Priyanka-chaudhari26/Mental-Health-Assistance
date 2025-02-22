from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

def custom_exception_handler(exc, context):
    # Handle token expiration errors
    if isinstance(exc, (TokenError, InvalidToken)):
        return Response({'detail': 'Please login again.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Call DRF's default exception handler for other errors
    response = exception_handler(exc, context)
    return response
