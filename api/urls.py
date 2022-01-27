from django.urls import path
from .views import homeView, CategoryList, GetCategory, PostList, GetPost, PostListByCategory, PostListByAuthor

urlpatterns = [
	path('', homeView, name='apiHome'),
	path('category/', CategoryList.as_view()),
	path('category/<int:pk>', GetCategory.as_view()),
	path('post/', PostList.as_view()),
	path('post/<int:pk>', GetPost.as_view()),
	path('post/by/category/<int:pk>', PostListByCategory.as_view()),
	path('post/by/author/<int:pk>', PostListByAuthor.as_view()),
]