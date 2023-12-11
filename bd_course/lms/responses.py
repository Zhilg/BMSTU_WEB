from rest_framework import status
from rest_framework.response import Response


OK = Response(status=status.HTTP_200_OK, data={'message': "Successfull operation"})

BAD_REQUEST = Response(status=status.HTTP_400_BAD_REQUEST, data={'message': "Bad request"})
UNAUTHORIZED = Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': "Invalid login or password"})

FAILED = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'message' : "Failed"})

