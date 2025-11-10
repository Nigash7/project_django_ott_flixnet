from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.admin,name= 'admin'),
    path('changepassword/',views.changepassword,name= 'changepassword'),
    path('adminhome/',views.listingpage,name= 'adminhome'),
    # path('adminnav/',views.adminnav,name= 'adminnav'),
    path('adminuserview/',views.adminuserview,name= 'adminuserview'),
    path('addmovie/',views.addmovie,name= 'addmovie'),
    path('viewdetails/',views.viewdetails,name= 'viewdetails'),
    path('userhistory/',views.userhistory,name= 'userhistory'),
    path('reporttop/',views.reporttop,name= 'reporttop'),
    path('logout2/',views.logout_page,name= 'logout2'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('view_movie/<int:movie_id>/', views.view_movie, name='view_movie'),
    path('user_history/<int:user_id>/', views.user_history, name='user_history'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('reporttop/', views.reporttop, name='reporttop'),






  

    
]