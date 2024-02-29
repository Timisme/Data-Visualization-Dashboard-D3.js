import django_filters
from .models import DataPoint

class DataPointFilter(django_filters.FilterSet):
    class Meta:
        model = DataPoint
        fields = ['end_year', 'sector', 'region', 'country', 'pestle']  #TODO: ADD 'source'