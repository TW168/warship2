# config/warehouse/urls.py 

from django.urls import path
from . import views


urlpatterns = [
    # path('hourly-stats/', views.hourly_stacker_stats, name='hourly-stats'),
    # path('ash-heatmap/', views.ash_event_heatmap, name='ash-heatmap'),
    # path('hourly-stats/', views.hourly_stacker_stats, name='hourly-stats'),
    path('dashboard/', views.warehouse_dashboard, name='warehouse-dashboard'),
]
