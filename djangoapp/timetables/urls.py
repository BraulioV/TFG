from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^senddata/$', views.senddata, name='senddata'),
	url(r'^(?P<days>[0-9]+)/(?P<hours>[0-9]+)/showdata/$', views.showdata, name='showdata'),
]
