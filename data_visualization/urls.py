# data_visualization/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('data-points/', views.DataPointList.as_view(), name='data-point-list'),
    path('api/data/', views.DataPointList.as_view(), name='data-list'),
    path('api/data/chart1/',  views.Chart1DataView.as_view(), name='Chart1DataView')
]
