from django.urls import path,include
from enteproject import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login, name='userlogin'),
    path('register', views.user_register, name='userregister'),
    path('home',views.home,name='home'),
    path('complaint',views.complaint,name='complaint'),
    path('menu/', views.todaysmenu, name='menu'),
    path('menu/<str:type>/', views.todaysmenu, name='menu_type'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('addmenu',views.addmenu,name='addmenu'),
    path('orderconfirm/<int:menu_id>/', views.placeorder, name='orderconfirm'),
    path('mybookings/', views.mybookings, name='mybookings'),
    path('addsuggestion',views.addsuggestion,name='addsuggestion'),
    path('adminsuggestionview',views.viewsuggestions,name='adminsuggestionview'),
    path('viewbookings',views.viewbookings,name='viewbookings'),
    path('bookingdone/<int:id>/',views.bookingdone,name='bookingdone'),
    path('profile/',views.profile,name='profile'),
    path('admincomplaint/',views.admincomplaints,name='admincomplaint'),
]