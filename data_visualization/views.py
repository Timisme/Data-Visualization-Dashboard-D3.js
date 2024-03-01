from collections import defaultdict

from django.db.models import Count, Avg
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DataPoint
from .serializers import DataPointSerializer
from .filters import DataPointFilter
from .utils import COUNTRY_CODE_MAPPER, generate_month_dates


# Create your views here.

class DataPointList(APIView):
    def get(self, request, format=None):
        data_points = DataPoint.objects.all()
        serializer = DataPointSerializer(data_points, many=True)
        return Response(serializer.data)

class TopicDonutDataView(APIView):
    def get(self, request, format=None):
        queryset = DataPoint.objects.exclude(topic__isnull=True)
        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs.values('topic').annotate(count=Count('id'))

        COUNT_THRESHOLD = 0
        others_data = {"topic": "others", "count": 0}
        result = []

        for data in list(queryset):
            if data["count"] <= COUNT_THRESHOLD:
                others_data["count"] += data["count"]
            else:
                result.append(data)

        if others_data["count"] != 0:
            result.append(others_data)

        return Response(result)

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

class LineChartDataView(APIView):
    def get(self, request, format=None):

        # data for line chart (time series) count: 114
        queryset = DataPoint.objects.filter(
            start_year__isnull=False,
            end_year__isnull=False,
            likelihood__isnull=False,
            intensity__isnull=False
        )

        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs

        result = []

        for instance in queryset:
            dates = generate_month_dates(instance.start_year, instance.end_year)
            for date in dates:
                result.append({
                    "date": date,
                    "intensity": instance.intensity,
                    "likelihood": instance.likelihood
                })

        # defaultdict to accumulate intensity, likelihood, and count for each date
        date_data = defaultdict(lambda: {"intensity": 0, "likelihood": 0, "count": 0})

        # Accumulate intensity, likelihood, and count for each date
        for item in result:
            date = item["date"]
            if date < "2030-01-01":
                date_data[date]["intensity"] += item["intensity"]
                date_data[date]["likelihood"] += item["likelihood"]
                date_data[date]["count"] += 1

        # Calculate average intensity and likelihood for each date
        data = [{
            "date": date,
            "average_intensity": date_data[date]["intensity"] / date_data[date]["count"],
            "average_likelihood": date_data[date]["likelihood"] / date_data[date]["count"]}
            for date in date_data
        ]

        return Response(data)

def _get_filter_config(exclude_fields=[]) -> dict:
    filter_fields = [field for field in DataPointFilter.Meta.fields if field not in exclude_fields]
    filter_config = {}
    for field_name in filter_fields:
        filter_config[field_name] = list(DataPoint.objects.values_list(field_name, flat=True).distinct())
    return filter_config

def dashboard(request):
    filter_fields = DataPointFilter.Meta.fields
    filter_config = {}
    for field_name in filter_fields:
        filter_config[field_name] = list(DataPoint.objects.values_list(field_name, flat=True).distinct())
    return render(request, "dashboard.html", context={
        "filter_config": filter_config
    })

def map(request):
    filter_config = _get_filter_config(["country", "region"])
    return render(request, "map.html", context={
        "filter_config": filter_config
    })

def distribution(request):
    filter_config = _get_filter_config(["sector", "topic"])
    return render(request, "distribution.html", context={
        "filter_config": filter_config
    })

def bar(request):
    filter_config = _get_filter_config()
    return render(request, "bar.html", context={
        "filter_config": filter_config
    })

def line(request):
    filter_config = _get_filter_config(["start_year", "end_year"])
    return render(request, "line.html", context={
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