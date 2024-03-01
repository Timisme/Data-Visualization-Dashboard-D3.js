# data_visualization/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("map/", views.map, name="map"),
    path("distribution/", views.distribution, name="distribution"),
    path("bar/", views.bar, name="bar"),
    path("line/", views.line, name="line"),
    path('data-points/', views.DataPointList.as_view(), name='data-point-list'),
    path('api/data/', views.DataPointList.as_view(), name='data-list'),
    path('api/data/chart1/',  views.TopicDonutDataView.as_view(), name='TopicDonutDataView'),
    path('api/data/chart2/',  views.Chart2DataView.as_view(), name='Chart2DataView'),
    path('api/data/chart3/',  views.Chart3DataView.as_view(), name='Chart3DataView'),
    path('api/data/chart4/',  views.Chart4DataView.as_view(), name='Chart4DataView'),
    path('api/data/chart5/',  views.MapDataView.as_view(), name='Chart5DataView'),
    path('api/data/chart6/',  views.LineChartDataView.as_view(), name='Chart6DataView'),

]
