from django.db.models import Count
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DataPoint
from .serializers import DataPointSerializer
from .filters import DataPointFilter


# Create your views here.

class DataPointList(APIView):
    def get(self, request, format=None):
        data_points = DataPoint.objects.all()
        serializer = DataPointSerializer(data_points, many=True)
        return Response(serializer.data)

class Chart1DataView(APIView):
    def get(self, request, format=None):
        # queryset = DataPoint.objects.exclude(country__isnull=True).exclude(topic__isnull=True)
        # queryset = queryset.values('country', 'topic').annotate(count=Count('id'))
        queryset = DataPoint.objects.exclude(country__isnull=True)
        filter = DataPointFilter(request.GET, queryset=queryset)
        filtered_queryset = filter.qs
        queryset = filtered_queryset.values('country').annotate(count=Count('id'))
        return Response(list(queryset))

def get(self, request, format=None):
    queryset = DataPoint.objects.all()

    # Example for filtering by year
    year = request.query_params.get('year')
    if year is not None:
        queryset = queryset.filter(year=year)

    # Implement other filters similarly

    serializer = DataPointSerializer(queryset, many=True)
    return Response(serializer.data)

def dashboard(request):
    filter_fields = DataPointFilter.Meta.fields
    filter_config = {}
    for field_name in filter_fields:
        filter_config[field_name] = list(DataPoint.objects.values_list(field_name, flat=True).distinct())
    return render(request, "dashboard.html", context={
        "filter_config": filter_config
    })
