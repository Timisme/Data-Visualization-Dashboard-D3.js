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
    path('api/data/chart2/',  views.RegionIntensityBarView.as_view(), name='RegionIntensityBarView'),
    path('api/data/chart3/',  views.Chart3DataView.as_view(), name='Chart3DataView'),
    path('api/data/chart4/',  views.Chart4DataView.as_view(), name='Chart4DataView'),
    path('api/data/chart5/',  views.MapDataView.as_view(), name='Chart5DataView'),
    path('api/data/chart6/',  views.LineChartIntensityDataView.as_view(), name='Chart6DataView'),
    path('api/data/chart7/',  views.LineChartLikelihoodDataView.as_view(), name='Chart7DataView'),
    path('api/data/chart8/',  views.RegionLikelihoodBarView.as_view(), name='Chart8DataView'),
    path('api/data/chart9/',  views.RegionRelevanceBarView.as_view(), name='Chart9DataView'),
    path('api/data/chart10/',  views.CountryIntensityBarView.as_view(), name='Chart10DataView'),
    path('api/data/chart11/',  views.CountryLikelihoodBarView.as_view(), name='Chart11DataView'),
    path('api/data/chart12/',  views.CountryRelevanceBarView.as_view(), name='Chart12DataView'),
]
