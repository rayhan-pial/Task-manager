from .models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        # fields = ['id', 'user', 'title', 'completed']
        exclude = ['user', 'date']


class TodoDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = '__all__'
