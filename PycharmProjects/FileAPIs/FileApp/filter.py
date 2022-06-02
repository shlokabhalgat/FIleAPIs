import django_filters
from .models import *


class FileDataFilter(django_filters.FilterSet):
    class Meta:
        model = File
        fields = {
            'staff_name': ['icontains'],
            'age': ['exact', 'lt', 'gt'],
            'year_joined': ['exact', 'gt', 'lt'],
            'position': ['icontains']
        }
