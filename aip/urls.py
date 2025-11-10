
from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.Signup,name='signup'),
    path('login/',views.login,name='login'),
    path('movies/',views.movie_list,name='movie-list'),
    path('movies/<int:movie_id>/',views.select_movie,name='select-movie'),
    path('watchlist/<int:movie_id>/',views.watchlist_view,name='watchlist-view'),
    path('watchlist/',views.get_watchlist,name='get-watchlist'),
    path('history/<int:movie_id>/',views.history,name='history-view'),
    path('history/',views.get_history,name='get-history'),
    path('watchlist_delete/<int:movie_id>/',views.delete_watchlist,name='delete-watchlist'),
    path('logout/',views.logout,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    


    
]