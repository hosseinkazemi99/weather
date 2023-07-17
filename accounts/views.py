from random import randint
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permission import IsOwnerOrReadOnly
from .weather import get_weather_status
from .models import Post
from .serializers import RegisterUserSerializer, ValidatePhoneSerializer, PostSerializer
from . import tasks
import redis
from django.contrib.auth.models import User

redis_host = "localhost"
redis_port = 6379
redis_connection = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


# give phone if valid send OTP
class RegisterUser(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        seializer = RegisterUserSerializer(data=request.data)
        seializer.is_valid(raise_exception=True)
        phone = seializer.validated_data['mobile_number']
        if redis_connection.get(name=phone) is None:
            otp = str(randint(100000, 999999))
            print(otp)
            tasks.sendotp.delay(phone, otp)
            return Response(status=status.HTTP_200_OK)

        return Response({'result': 'send code recently'})


# register phone_number
class ValidatePhone(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ValidatePhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['mobile_number']
        otp2 = redis_connection.get(phone)
        otp_client = serializer.validated_data['otp']
        print(otp2)
        if otp_client != otp2:
            return Response(status.HTTP_401_UNAUTHORIZED)

        user, created = User.objects.get_or_create(username=phone)
        refresh = RefreshToken.for_user(user)
        response_data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'created': created
        }
        print(response_data.get('access_token'))

        return Response(response_data, status=status.HTTP_200_OK)


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            print(request.COOKIES)
            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CreatePost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        text = serializer.validated_data['text']
        if Post.objects.filter(title=title).exists():
            return Response(data={'error': 'title has already exist'}, status=status.HTTP_409_CONFLICT)
        Post.objects.create(text=text, title=title, owner=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReadPost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, slug_id):
        try:
            post = Post.objects.get(slug=slug_id)
        except:
            return Response(status.HTTP_404_NOT_FOUND)

        respons_data = {
            "User": post.owner.username,
            "title": post.title,
            "text": post.text,
            "created_at": post.created_at,
            "modified_at": post.modified_at,
        }
        return Response(respons_data, status=status.HTTP_200_OK)


class UpdatePost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, slug_id):
        try:
            post = Post.objects.get(slug=slug_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if Post.objects.filter(title=serializer.validated_data['title']).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class DeletePost(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, slug_id):
        try:
            post = Post.objects.get(slug=slug_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response(status=status.HTTP_200_OK)



class WeatherView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        city = request.data.get('city')  # Get the city from the request data
        if not city:
            return Response({'error': 'City parameter is required'}, status=400)

        weather_status = get_weather_status(city)

        return Response({'weather_status': weather_status})
