# data_visualization/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('data-points/', views.DataPointList.as_view(), name='data-point-list'),
    path('api/data/', views.DataPointList.as_view(), name='data-list'),
    path('api/data/chart1/',  views.Chart1DataView.as_view(), name='Chart1DataView'),
    path('api/data/chart2/',  views.Chart2DataView.as_view(), name='Chart2DataView'),
    path('api/data/chart3/',  views.Chart3DataView.as_view(), name='Chart3DataView'),
    path('api/data/chart4/',  views.Chart4DataView.as_view(), name='Chart4DataView'),
    path('api/data/chart5/',  views.MapDataView.as_view(), name='Chart5DataView'),

]
