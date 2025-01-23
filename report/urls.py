# config/report/urls.py 

from django.urls import path
from .views import report, submit_report



urlpatterns = [
    # path('hourly-stats/', views.hourly_stacker_stats, name='hourly-stats'),
    # path('ash-heatmap/', views.ash_event_heatmap, name='ash-heatmap'),
    # path('hourly-stats/', views.hourly_stacker_stats, name='hourly-stats'),
    path('report/', report, name='report'),
    path('submit/', submit_report, name='submit_report'),
]