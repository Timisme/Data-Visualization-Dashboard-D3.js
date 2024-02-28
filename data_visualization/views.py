from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DataPoint
from .serializers import DataPointSerializer


# Create your views here.

def datapoint_list(request):
    datapoints = DataPoint.objects.all()
    serializer = DataPointSerializer(datapoints, many=True)
    return Response(serializer.data, safe=False)


class DataPointList(APIView):
    def get(self, request, format=None):
        data_points = DataPoint.objects.all()
        serializer = DataPointSerializer(data_points, many=True)
        return Response(serializer.data)


def get(self, request, format=None):
    queryset = DataPoint.objects.all()

    # Example for filtering by year
    year = request.query_params.get('year')
    if year is not None:
        queryset = queryset.filter(year=year)

    # Implement other filters similarly

    serializer = DataPointSerializer(queryset, many=True)
    return Response(serializer.data)
