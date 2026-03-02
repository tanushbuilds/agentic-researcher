from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('run/', views.run_research, name='run_research'),
    path('memory/', views.memory, name='memory'),
    path('memory/delete/<str:key>/', views.delete_memory, name='delete_memory'),
    path('memory/clear/', views.clear_memory, name='clear_memory'),
]