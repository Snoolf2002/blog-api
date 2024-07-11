from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import UserView, Users, PostsView, PostView

urlpatterns = [
    path('users/<int:id>/', UserView.as_view()),
    path('users/', Users.as_view()),
    path('posts/', PostsView.as_view()),
    path('posts/<int:id>/', PostView.as_view()),

    # JWT
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]