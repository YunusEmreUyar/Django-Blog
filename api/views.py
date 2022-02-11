from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from users.models import Profile
from rest_framework import status
from blog_post.models import Category, Post, Comment
from .serializers import (
	CategorySerializer,
 	PostSerializer,
	PartialUserSerializer,
	ProfileSerializer,
	PostSerializer,
	CommentSerializer,
	RegisterSerializer)


def homeView(request):
	content = """
	api/
		category/
			/ Returns list of all category items.
			/<int:id>/ Get 1 category object that has the id.
		post/
			/ Returns list of all post items.
			/<int:id>/ Returns a post item that has id given to url.
			/by/category/<int:id>/ Get 1 post with category number given to url.
			/by/author/<int:id>/ Get all posts of author given in url.
		user/
			/<str:username>/ Returns fields of User db model for given username.
		token/
			/ Returns authentication token for provided username and password match.
			Takes username and password in body.
		token-refresh/
			/ Returns token refresh. Takes username and password in body.
		comment/
			/<int:id> Returns all comments of the post that has given id.
			/create/<int:postId>/ Create comment object to given obj.
		like/
			/<int:postId>/ Updates post like field of the post that has given id. 
			Takes userId and postId to like.
		register/
			/ Registers a new user object with given username, password, password2 and email.
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
		posts = Post.objects.all().order_by('-date_created')
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


class PostListByCategory(APIView):
	"""
	Get posts list from given category.
	"""
	def get(self, request, pk, format=None):
		posts = get_list_or_404(Post, category=pk)
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class PostListByAuthor(APIView):
	"""
	Get posts list of given author.
	"""
	def get(self, request, pk, format=None):
		posts = get_list_or_404(Post, author=pk)
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllCommentsToGivenPost(APIView):
	"""
	Get all comments for provided post.
	"""
	def get(self, request, pk, format=None):
		comments = get_list_or_404(Comment, post=pk)
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class LikePost(APIView):
	"""
	Like a post object.
	"""
	authentication_classes = (JWTAuthentication,)
	permission_classes = [IsAuthenticated]

	def put(self, request, postId, format=None):
		post = get_object_or_404(Post, pk=postId)
		user = self.request.user
		data = {"liked": False}
		if not user in post.likes.all():
			data["liked"]= True
			data["updated"] = True
			post.likes.add(user)
			return Response(data)
		data["liked"] = True
		data["updated"] = False
		return Response(data)


class GetUserByUsername(APIView):
	"""
	Get User obj from given username.
	"""
	def get(self, request, username, format=None):
		user = get_object_or_404(User, username=username)
		data = {"username": username, "id":user.id}
		return Response(data, status=status.HTTP_200_OK)


class CreateComment(APIView):
	"""
	Create comment obj for given post.
	"""
	authentication_classes = (JWTAuthentication,)
	permission_classes = [IsAuthenticated,]          

	def put(self, request, pk, format=None):
		post = get_object_or_404(Post, pk=pk)
		user = self.request.user
		data = self.request.data
		if data.content:
			comment = Comment(post=post, created_by=user, content=data.content)
			comment.save()
			return Response(comment)
		return Response({"detail": "Wrong input"})


class RegisterView(CreateAPIView):
	queryset = User.objects.all()
	permission_classes = (AllowAny,)
	serializer_class = RegisterSerializer