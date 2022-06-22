from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

        # def create(self, validated_data):
        #     user = User.objects.create(username=validated_data['username'])
        #     user.set_name(validated_data['name'])
        #     user.set_password(validated_data['password'])
        #     user.set_email(validated_data['email'])
        #     user.save()
        #     return user


class PostSerializer(serializers.ModelSerializer):
    # user=UserSerializer()
    class Meta:
        model=Post
        fields="__all__"


