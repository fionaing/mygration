from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'), #homepage for plans!
    path('about', views.about, name='home.about'), #individual plan vie w
    path('dashboard/', views.dashboard, name='dashboard'),

    path('plans/<int:id>/', views.show, name='plan.show'),
    path('plans/<int:id>/join/', views.join_plan, name='plan.join'),
    path('plans/<int:id>/comment/', views.add_comment, name='plan.comment'),

]

