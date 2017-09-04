from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ColumnView.as_view(), name='column_detail'),
]
