from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile
from blog_post.models import Category, Post, Comment

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
		fields = ['username', 'profile']


class PostSerializer(serializers.ModelSerializer):
	author = PartialUserSerializer(many=False, read_only=True)
	#content = strip_tags(content)

	class Meta:
		model = Post
		fields = '__all__'
