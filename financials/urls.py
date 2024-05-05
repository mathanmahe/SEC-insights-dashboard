from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insights/', views.insights, name='insights'),
    path('visualizations/', views.visualizations, name='visualizations'),
    path('loadData/', views.loadData, name='load-data' )
]
