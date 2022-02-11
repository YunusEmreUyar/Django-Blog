from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile
from blog_post.models import Category, Post, Comment
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

	def create(self, validated_data):
		category = Category(name=validated_data)
		category.save()
		return category


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['description', 'profile_pic',]


class PartialUserSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer(many=False, read_only=True)
	class Meta:
		model = User
		fields = ['username', 'profile', 'id']

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
	author = PartialUserSerializer(many=False, read_only=True)
	category = CategorySerializer(many=False, read_only=True)

	class Meta:
		model = Post
		fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
	created_by = PartialUserSerializer(many=False, read_only=True)

	class Meta:
		model = Comment
		fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
	    model = User
	    fields = ('username', 'password', 'password2', 'email')

	def validate(self, attrs):
	    if attrs['password'] != attrs['password2']:
	        raise serializers.ValidationError({"password": "Password fields didn't match."})

	    return attrs

	def create(self, validated_data):
	    user = User.objects.create(
	        username=validated_data['username'],
	        email=validated_data['email'],
	    )
	    user.set_password(validated_data['password'])
	    user.is_active = False
	    user.save()
	    return user