from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import UserManagerSerializers, UserLoginSerializers, UserProfileSerializers, UserChangePasswordSerializers, SendPasswordResetEmailSerializers, UserpasswordResetSerializers
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from .models import User
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

"""Generate Token manuallyu"""
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    """Registering User"""
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = UserManagerSerializers(data=request.data)
        if serializer.is_valid():
            user= serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """Login User"""
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = UserLoginSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg':'Login Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non-field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileview(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializers

    def get_object(self):
        return self.request.user

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = UserChangePasswordSerializers(data=request.data)
        if serializer.is_valid():
            password = serializer.data.get('password')
            request.user.set_password(password)
            request.user.save()
            return Response({'msg':'Pass change Successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self,request):
        serializer=SendPasswordResetEmailSerializers(data=request.data)
        if serializer.is_valid():
            return Response({'msg':'Pass Reset Link send, Please check Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,uid, token):
            serializer=UserpasswordResetSerializers(data=request.data, context={'uid':uid, 'token':token})
            if serializer.is_valid():
                return Response({'msg':'Pass change Successful'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)