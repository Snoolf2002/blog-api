from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Post
from .serializers import PostSerializer


class UserView(APIView):
    def get(self, request, id:int):
        try:
            user = User.objects.get(id=id)
            return Response({ "username": user.username, "first_name": user.first_name, "last_name": user.first_name})
        except:
            return Response({'result':'User not found'})
        

class Users(APIView):
    def get(self, request):
        try:
            data = []
            users = User.objects.all()
            for user in users:
                data.append({ "username": user.username, "first_name": user.first_name, "last_name": user.first_name})
            return Response(data)
        except:
            return Response({'result':'Users not found'})

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        if username == None or password == None:
            return Response({'result':'didn\'t input required data'})
        try:
            user=User.objects.get(username=username)
            return Response({'result':'Invalid username'})
        except:
            user=User.objects.create(
                username = username,
                password = make_password(password),
                first_name = first_name,
                last_name = last_name
            )
            user.save()
            return Response({ "message": "User created successfully." }, status=status.HTTP_201_CREATED)
        

class PostsView(APIView):
    def get(self, request: Request) -> Response:
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response({"posts": serializer.data})
    
    def post(self, request: Request) -> Response:
        data = request.data
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post created successufully"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
        # title = data.get('title', None)
        # content = data.get('content', None)
        # author = data.get('author', None)

        # if title == None or content == None or author == None:
        #     return Response({"error": "You have to fill all fields!"})
        # else:
        #     try:
        #         user = User.objects.get(id=int(author))
        #     except User.DoesNotExist:
        #         user = None
        #         return Response({"error": "User didn't find."})

        #     if user is not None:
        #         blog = Post.objects.create(
        #             title = title,
        #             content = content,
        #             author = user
        #         )
        #         blog.save()
        #         return Response({"message": "Blog successufully created."}, status=status.HTTP_201_CREATED)
    

class PostView(APIView):
    def get(self, request: Request, id: int) -> Response:
        try:
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Status": "This post doesn't exist."}, status=status.HTTP_404_NOT_FOUND)