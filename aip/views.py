from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
# from django.contrib.auth.models import User
# from app.models import User
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from app.models import movie
from rest_framework import status
from aip.serializers import MovieSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from app.models import watchlist
from app.models import history_view



User = get_user_model()



@api_view(['POST'])
@permission_classes((AllowAny,))
def Signup(request):
        email  = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        if not name or not email or not password:
            return Response({'message':'All fields are required'})
        if User.objects.filter(email=email).exists():
            return  JsonResponse({'message':'Email already exist'})
            
        user = User.objects.create_user(email=email,password=password,name=name )
        # user.name = name
        # user.save()
        return JsonResponse({'message':'user created successfully'} ,status = 200)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

 
@api_view(['GET'])
@permission_classes((AllowAny,))
def movie_list(request):
    movies = movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def select_movie(request,movie_id):
   movies=get_object_or_404(movie,id=movie_id)
   serializer=MovieSerializer(movies)
   return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def watchlist_view(request, movie_id):
    user = request.user
    existing_item = watchlist.objects.filter(movie_id=movie_id, user=user).first()

    if existing_item:
        existing_item.delete()
        return Response({'message': 'Movie removed from watchlist'}, status=status.HTTP_200_OK)
    else:
        watchlist.objects.create(movie_id=movie_id, user=user)
        return Response({'message': 'Movie added to watchlist'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    user = request.user.id
    items = watchlist.objects.filter(user_id=user)
    serializer = MovieSerializer([item.movie for item in items], many=True)
    return Response(serializer.data)  
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_watchlist(request,movie_id):
    user = request.user.id
    item = watchlist.objects.filter(movie_id=movie_id,user_id=user)
    item.delete()
    return Response({'message': 'Movie removed from watchlist'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def history(request,movie_id):
    user = request.user.id
    
    item = history_view.objects.create(movie_id=movie_id,user_id=user)
    
    item.save()

    return Response({'message': 'Movie added to history'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    user = request.user.id
    items = history_view.objects.filter(user_id=user)
    serializer = MovieSerializer([item.movie for item in items], many=True)
    return Response(serializer.data)
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def delete_history(request,movie_id):
#     user = request.user.id
#     item = history_view.objects.filter(movie_id=movie_id,user_id=user)
#     item.delete()
#     return Response({'message': 'Movie removed from history'}, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    print(old_password,new_password)

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)   
      


    

# Create your views here.
