from collections import defaultdict

from django.db.models import Count, Avg
from django.shortcuts import render
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DataPoint
from .serializers import DataPointSerializer
from .filters import DataPointFilter
from .utils import COUNTRY_CODE_MAPPER, generate_month_dates


# Rest API views

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

        COUNT_THRESHOLD = 5

        sorted_data = sorted(list(queryset), key=lambda x: x["count"], reverse=True)
        if len(sorted_data) > COUNT_THRESHOLD:
            return Response(sorted_data[:COUNT_THRESHOLD])

        return Response(sorted_data)

class RegionIntensityBarView(APIView):
    category_field = "region"
    value_field = "intensity"

    def get(self, request, format=None):
        kwargs = {f"{self.category_field}__isnull": False, f"{self.value_field}__isnull": False}
        queryset = DataPoint.objects.filter(**kwargs)
        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs.values(self.category_field).annotate(value=Avg(self.value_field))

        result = []
        for data in list(queryset):
            data["category"] = data.pop(self.category_field)
            result.append(data)

        return Response(result)

class RegionLikelihoodBarView(RegionIntensityBarView):
    category_field = "region"
    value_field = "likelihood"

class RegionRelevanceBarView(RegionIntensityBarView):
    category_field = "region"
    value_field = "relevance"

class CountryIntensityBarView(RegionIntensityBarView):
    category_field = "country"
    value_field = "intensity"

class CountryLikelihoodBarView(RegionIntensityBarView):
    category_field = "country"
    value_field = "likelihood"

class CountryRelevanceBarView(RegionIntensityBarView):
    category_field = "country"
    value_field = "relevance"

class SectorPieChartDataView(APIView):
    def get(self, request, format=None):
        queryset = DataPoint.objects.exclude(sector__isnull=True)
        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs.values('sector').annotate(count=Count('id'))

        COUNT_THRESHOLD = 5

        sorted_data = sorted(list(queryset), key=lambda x: x["count"], reverse=True)
        if len(sorted_data) > COUNT_THRESHOLD:
            return Response(sorted_data[:COUNT_THRESHOLD])

        return Response(sorted_data)

class Chart4DataView(APIView):
    def get(self, request, format=None):
        result = []
        for category in ["intensity", "likelihood", "relevance"]:
            kwargs = {f"{category}__isnull": True}
            queryset = DataPoint.objects.exclude(region__isnull=True).exclude(**kwargs)
            filter = DataPointFilter(request.GET, queryset=queryset)
            queryset = filter.qs.values('region').annotate(value=Avg(category))
            for data in list(queryset):
                data["category"] = category
                result.append(data)
        return Response(result)

class MapDataView(APIView):
    def get(self, request, format=None):
        queryset = DataPoint.objects.exclude(country__isnull=True)
        filter = DataPointFilter(request.GET, queryset=queryset)
        queryset = filter.qs.values('country').annotate(
            count=Count("id"),
            avg_intensity=Avg("intensity"),
            avg_likelihood=Avg("likelihood"),
            avg_relevance=Avg("relevance"),
        )

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
                    "count": 0,
                    "avg_intensity": 0,
                    "avg_likelihood": 0,
                    "avg_relevance": 0
                })

        return Response(result)

def _get_sorted_line_data(queryset, value_field = "intensity") -> list:
    result = []
    for instance in queryset:
        dates = generate_month_dates(instance.start_year, instance.end_year)
        for date in dates:
            result.append({
                "date": date,
                value_field: getattr(instance, value_field),
            })

    # defaultdict to accumulate intensity, likelihood, and count for each date
    date_data = defaultdict(lambda: {value_field: 0, "count": 0})

    # Accumulate intensity, likelihood, and count for each date
    for item in result:
        date = item["date"]
        if date < "2030-01-01":
            date_data[date][value_field] += item[value_field]
            date_data[date]["count"] += 1

    # Calculate average intensity and likelihood for each date
    data = [{
            "date": date,
            "value": date_data[date][value_field] / date_data[date]["count"]
        }
        for date in date_data
    ]

    return sorted(data, key=lambda x: x["date"])

class LineChartIntensityDataView(APIView):
    def get(self, request, format=None):
        # data for line chart (time series) count: 114
        queryset = DataPoint.objects.filter(
            start_year__isnull=False,
            end_year__isnull=False,
            likelihood__isnull=False,
            intensity__isnull=False
        )

        filter = DataPointFilter(request.GET, queryset=queryset)
        sorted_data = _get_sorted_line_data(filter.qs)
        return Response(sorted_data)

class LineChartLikelihoodDataView(APIView):
    def get(self, request, format=None):
        # data for line chart (time series) count: 114
        queryset = DataPoint.objects.filter(
            start_year__isnull=False,
            end_year__isnull=False,
            likelihood__isnull=False,
            intensity__isnull=False
        )
        filter = DataPointFilter(request.GET, queryset=queryset)
        sorted_data = _get_sorted_line_data(filter.qs, "likelihood")
        return Response(sorted_data)

def _get_filter_config(exclude_fields=[], not_null_fields=[]) -> dict:
    filter_fields = [field for field in DataPointFilter.Meta.fields if field not in exclude_fields]
    filter_config = {}
    for field_name in filter_fields:

        exclude_kwargs = {field_name: None}

        if not_null_fields:
            q_objects = [Q(**{f"{field}__isnull": False}) for field in not_null_fields]
            combined_q_objects = Q()
            for q_object in q_objects:
                combined_q_objects &= q_object

            print(combined_q_objects)

            options = list(
                DataPoint.objects
                    .exclude(**exclude_kwargs)
                    .filter(combined_q_objects)
                    .values_list(field_name, flat=True)
                    .distinct()
                )
        else:
            options = list(DataPoint.objects.exclude(**exclude_kwargs).values_list(field_name, flat=True).distinct())

        options.sort()
        filter_config[field_name] = options

    return filter_config


# template rendering views

def dashboard(request):
    return render(request, "dashboard.html", context={
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
    filter_config = _get_filter_config(
        exclude_fields=["start_year", "end_year"],
        not_null_fields=["intensity", "likelihood", "relevance"]
    )
    return render(request, "bar.html", context={
        "filter_config": filter_config
    })

def line(request):
    filter_config = _get_filter_config(
        exclude_fields=["start_year", "end_year"],
        not_null_fields=["intensity", "likelihood", "start_year", "end_year"]
    )
    return render(request, "line.html", context={
        "filter_config": filter_config
    })