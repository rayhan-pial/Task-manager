from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from authenticate.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import TodoSerializer, TodoDetailsSerializer
from .models import Todo
from authenticate.models import User
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class TodoListCreateView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        if self.request.method == 'POST':
            # Use Todo.objects.all() queryset for creating new todos
            return Todo.objects.all()
        else:
            # Use Todo.objects.filter(user=self.request.user) queryset for listing todos
            return Todo.objects.filter(user=self.request.user)


    def get_serializer_class(self):
        if self.request.method == 'POST':
            # Use TodoSerializer for creating new todos
            return TodoSerializer
        else:
            # Use TodoDetailsSerializer for listing todos
            return TodoDetailsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # instance = self.perform_create(serializer)
        instance = serializer.save(user=self.request.user)
        # headers = self.get_success_headers(serializer.data)
        serializer = TodoDetailsSerializer(instance=instance, many = False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TodoListretriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    # serializer_class = TodoSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            # Use TodoSerializer for creating new todos
            return TodoDetailsSerializer
        else:
            # Use TodoDetailsSerializer for listing todos
            return TodoSerializer
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
