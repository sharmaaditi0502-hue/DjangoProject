from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), 
    path('contact/', views.contact, name='contact'), 
    path('menu/', views.menu, name='menu'), 
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('users_list/',views.users_list,name='users_list'),
    path('billing/',views.billing,name='billing'),
    path('order_success/',views.order_success,name='order_success'),
    path('order_history/',views.order_history,name='order_history'),
 
    


]