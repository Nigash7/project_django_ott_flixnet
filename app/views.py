from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from app.models import movie
from app.models import history_view
from app.models import User
from django.db.models import Count
from .models import watchlist
from django.core.paginator import Paginator

from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

@never_cache
def admin(request):
    if request.user.is_authenticated and request.user.is_admin:
        return redirect('adminhome')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_admin:
            login(request, user)
            return redirect("adminhome")
            request.session.flush()
        else:
            error = "Invalid credentials or not an admin user."
            return render(request, "admin.html", {'error': error})
    return render(request, "admin.html") 
        
        
    
@csrf_protect
@login_required(login_url='admin')
@never_cache
def changepassword(request):
    if request.method =='POST':
        current_password=request.POST.get('current_password')
        new_password=request.POST.get('new_password')

        user=request.user
        if not user.check_password(current_password):
            error="Current password is incorrect."
            return render(request,"changepassword.html",{'error':error})
        else:
            user.set_password(new_password)
            user.save()
            logout(request) 
            messages.success(request, 'Password changed successfully. Please log in again.')
            return redirect('admin')
    return render(request,"changepassword.html")

@permission_classes([IsAuthenticated])
def listingpage(request):
        query = request.GET.get('search') 
        movies=movie.objects.all().order_by('-id')
        if query:
           search_movies = movie.objects.filter(title__icontains=query)
           other_movies= movies.exclude(id__in=search_movies)
           movies = list(search_movies) + list(other_movies)
          

        return render(request, "listingpage.html", {'movies':movies,'query': query})

# def adminnav(request):
#     return render(request,"adminnav.html")
@permission_classes([IsAuthenticated])     
def adminuserview(request):
    search_query = request.GET.get('search', '')  # get search value from URL

    if search_query:
        users = User.objects.filter(name__icontains=search_query).order_by('-id')
    else:
        users = User.objects.all().order_by('-id')

    return render(request, 'adminuserview.html', {'users': users})

@permission_classes([IsAuthenticated])
def addmovie(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        title = request.POST.get('title')
        description = request.POST.get('description')

       
        if  not thumbnail or not  video_file or not title or not description :
            error = "All fields are required."
            return render(request, "addmovie.html", {'error': error})
        else:  
            movie.objects.create(
            video_file=video_file,
            thumbnail=thumbnail,
            title=title,
            description=description)
             
            return render(request, "addmovie.html", {'message': 'Movie added successfully!'})
    else:
        return render(request, "addmovie.html")    

    
    

    
def viewdetails(request):
    return render(request,"viewdetails.html")  
def userhistory(request):
    return render(request,"userhistory.html") 
def reporttop(request):
    return render(request,"reporttop.html")   


@login_required(login_url='admin')
@never_cache
def logout_page(request):
    if request.method == 'POST':  # When the button is clicked
        logout(request)  # Logs out the user
        return redirect('admin')  # Redirect to login page after logout
    return render(request, 'logout.html')



def edit_movie(request, movie_id):
    movie_obj = get_object_or_404(movie, id=movie_id)

    if request.method == 'POST':
        movie_obj.title = request.POST.get('title')
        movie_obj.description = request.POST.get('description')

        if 'thumbnail' in request.FILES:
            movie_obj.thumbnail = request.FILES['thumbnail']
        if 'video_file' in request.FILES:
            movie_obj.video_file = request.FILES['video_file']

        movie_obj.save()
        return redirect('adminhome')  # after update go back to listing

    return render(request, 'edit_movie.html', {'movie': movie_obj})

def delete_movie(request, movie_id):
    mov = get_object_or_404(movie, id=movie_id)
    mov.delete()
    return redirect('adminhome')   
def view_movie(request, movie_id):
    mov = get_object_or_404(movie, id=movie_id)
    return render(request, "view_movie.html", {'movie': mov})



def user_history(request, user_id):
    user = get_object_or_404(User, id=user_id)
    history_items = history_view.objects.filter(user=user).order_by('-id')
    return render(request, 'user_history.html', {'user': user, 'history': history_items})



def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('adminuserview')

def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('adminuserview')


def reporttop(request):
    # Count how many times each movie was watched
    most_viewed = (
       watchlist.objects
        .values('movie__title')
        .annotate(view_count=Count('movie'))
        .order_by('-view_count')
    )

    # Top 5 movies
    top_movies = most_viewed[:5]

    return render(request, 'reporttop1.html', {'top_movies': top_movies})


# Create your views here.
