from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import (
	homeView, 
	CategoryList, 
	GetCategory, 
	PostList, 
	GetPost, 
	PostListByCategory, 
	PostListByAuthor, 
	GetAllCommentsToGivenPost,
	LikePost,
	GetUserByUsername,
	CreateComment,
	RegisterView
	)

urlpatterns = [
	path('', homeView),
	path('category/', CategoryList.as_view()),
	path('category/<int:pk>', GetCategory.as_view()),
	path('post/', PostList.as_view()),
	path('post/<int:pk>', GetPost.as_view()),
	path('post/by/category/<int:pk>', PostListByCategory.as_view()),
	path('post/by/author/<int:pk>', PostListByAuthor.as_view()),
	path('token', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token-refresh', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('comment/<int:pk>', GetAllCommentsToGivenPost.as_view()),
    path('like/<int:postId>', LikePost.as_view()),
    path('user/<str:username>', GetUserByUsername.as_view()),
    path('comment/create/<int:pk>', CreateComment.as_view()),
    path('register/', RegisterView.as_view())
]