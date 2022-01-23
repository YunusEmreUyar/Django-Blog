from django.urls import path
from .views import homeView, CategoryList, GetCategory, PostList, GetPost

urlpatterns = [
	path('', homeView, name='apiHome'),
	path('category/', CategoryList.as_view()),
	path('category/<int:pk>', GetCategory.as_view()),
	path('post/', PostList.as_view()),
	path('post/<int:pk>', GetPost.as_view()),
]