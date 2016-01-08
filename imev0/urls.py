__author__ = 'MiladDK'

__author__ = 'MiladDK'
from django.conf.urls import url
from .views import Index, Datas

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^datas$', Datas.as_view(), name='getDatas'),
]
