from django.urls import path
from .views import homeView, CategoryList, GetCategory, PostList, GetPost, PostListByCategory, PostListByAuthor
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
	path('', homeView, name='apiHome'),
	path('category/', CategoryList.as_view()),
	path('category/<int:pk>', GetCategory.as_view()),
	path('post/', PostList.as_view()),
	path('post/<int:pk>', GetPost.as_view()),
	path('post/by/category/<int:pk>', PostListByCategory.as_view()),
	path('post/by/author/<int:pk>', PostListByAuthor.as_view()),
	path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
]