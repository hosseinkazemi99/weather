from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('validate/', views.ValidatePhone.as_view(), name='otp'),
    path('home/', views.Home.as_view(), name='home'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createpost/', views.CreatePost.as_view(), name='createpost'),
    path('readpost/<slug:slug_id>/', views.ReadPost.as_view(), name= 'readpost'),
    path('updatepost/<slug:slug_id>/', views.UpdatePost.as_view(), name= 'updateposte'),
    path('deletepost/<slug:slug_id>/', views.DeletePost.as_view(), name= 'deletepost'),
    path('weather/', views.WeatherView.as_view(), name='weather'),
]





