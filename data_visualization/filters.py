import django_filters
from .models import DataPoint

class DataPointFilter(django_filters.FilterSet):
    class Meta:
        model = DataPoint
        fields = ['start_year', 'end_year', 'sector', 'region', 'country', 'pestle', 'topic']  #TODO: ADD 'source'