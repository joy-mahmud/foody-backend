from django.urls import path
from . import views

urlpatterns = [
    path('get-stats',views.stats_summary,name="get_stats")
]
