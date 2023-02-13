from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from users.serializers import UserSerializer
from users.models import User

class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()

        email = serializer.validated_data["email"]

        user_found = User.objects.filter(email__iexact=email).first()

        if user_found:
            return Response({"error": "User exists!"}, 400)

        user = User.objects.create(**serializer.validated_data)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_201_CREATED)
