from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from users.models import Profile
from rest_framework import status
from blog_post.models import Category, Post
from .serializers import (
	CategorySerializer,
 	PostSerializer, 
	PartialUserSerializer, 
	ProfileSerializer, 
	PostSerializer)

def homeView(request):
	content = """
	api/
		category/
			/ Returns list of all category items.
			<int:id>/ Get 1 category object that has the id.
		post/
			/ Returns list of all post items.
	"""
	return HttpResponse(content, 200)


class CategoryList(APIView):
	"""
	List all categories.
	"""
	def get(self, request, format=None):
		categories = Category.objects.all()
		serializer = CategorySerializer(categories, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class GetCategory(APIView):
	"""
	Get a category object.
	"""
	def get(self, request, pk, format=None):
		category = get_object_or_404(Category, pk=pk)
		serializer = CategorySerializer(category, many=False)
		return Response(serializer.data, status=status.HTTP_200_OK)


class PostList(APIView):
	"""
	Get all posts
	"""
	def get(self, request, format=None):
		posts = Post.objects.all()
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class GetPost(APIView):
	"""
	Get one post related to the given id.
	"""
	def get(self, request, pk, format=None):
		post = get_object_or_404(Post, pk=pk)
		serializer = PostSerializer(post, many=False)
		return Response(serializer.data, status=status.HTTP_200_OK)