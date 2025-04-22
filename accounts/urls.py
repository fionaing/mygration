from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('plans/', views.plans, name='accounts.plans'),
    path('reset_password/', views.reset_password, name='accounts.reset_password'),
    path('profile/', views.profile, name='accounts.profile'),
    path('add_plan/', views.add_plan, name='accounts.add_plan')
]