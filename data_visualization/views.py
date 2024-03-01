from django.db.models import Count, Avg
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DataPoint
from .serializers import DataPointSerializer
from .filters import DataPointFilter
from .utils import COUNTRY_CODE_MAPPER


# Create your views here.

class DataPointList(APIView):
    def get(self, request, format=None):
        data_points = DataPoint.objects.all()
        serializer = DataPointSerializer(data_points, many=True)
        return Response(serializer.data)

class Chart1DataView(APIView):
    def get(self, request, format=None):
        queryset = DataPoint.objects.exclude(topic__isnull=True)
        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs.values('topic').annotate(count=Count('id'))
        return Response(list(queryset))

class Chart2DataView(APIView):
    def get(self, request, format=None):
        queryset = DataPoint.objects.exclude(sector__isnull=True)
        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs.values('sector').annotate(count=Count('id'))
        return Response(list(queryset))

class Chart3DataView(APIView):
    def get(self, request, format=None):
        queryset = DataPoint.objects.exclude(sector__isnull=True)
        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs.values('sector').annotate(count=Count('id'))
        return Response(list(queryset))

class Chart4DataView(APIView):
    def get(self, request, format=None):
        # queryset = DataPoint.objects.exclude(country__isnull=True).exclude(topic__isnull=True)
        # queryset = queryset.values('country', 'topic').annotate(count=Count('id'))
        result = []
        for category in ["intensity", "likelihood", "relevance"]:
            kwargs = {f"{category}__isnull": True}
            queryset = DataPoint.objects.exclude(country__isnull=True).exclude(**kwargs)
            filter = DataPointFilter(request.GET, queryset=queryset)
            queryset = filter.qs.values('country').annotate(value=Avg(category))
            for data in list(queryset):
                data["category"] = category
                result.append(data)
        return Response(result)

class MapDataView(APIView):
    def get(self, request, format=None):
        queryset = DataPoint.objects.exclude(country__isnull=True)
        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs.values('country').annotate(count=Count("id"))

        result = []
        for data in list(queryset):
            data["code"] = COUNTRY_CODE_MAPPER[data["country"]] if data["country"] else None
            result.append(data)

        current_codes = [item["code"] for item in result]

        for country, code in COUNTRY_CODE_MAPPER.items():
            if code not in current_codes:
                result.append({
                    "country": country,
                    "code": code,
                    "count": 0
                })

        return Response(result)

def dashboard(request):
    filter_fields = DataPointFilter.Meta.fields
    filter_config = {}
    for field_name in filter_fields:
        filter_config[field_name] = list(DataPoint.objects.values_list(field_name, flat=True).distinct())
    return render(request, "dashboard.html", context={
        "filter_config": filter_config
    })

'''not used'''
def get(self, request, format=None):
    queryset = DataPoint.objects.all()

    # Example for filtering by year
    year = request.query_params.get('year')
    if year is not None:
        queryset = queryset.filter(year=year)

    # Implement other filters similarly

    serializer = DataPointSerializer(queryset, many=True)
    return Response(serializer.data)