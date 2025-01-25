from django.contrib.auth.models import User
from rest_framework.authentication import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import SignUpSerializer

# Create your views here.


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class LoginView(APIView):

    @classmethod
    def post(cls, request: Request) -> Response:
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user and isinstance(user, User):
            context = {
                "status": "success",
                "content": {
                    "username": user.username,
                    "first_name": user.first_name,
                },
            }
        else:
            context = {
                "status": "error",
                "content": "Invalid credentials",
            }

        return Response(context)
