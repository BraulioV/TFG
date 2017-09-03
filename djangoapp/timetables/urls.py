from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^senddata/$', views.senddata, name='senddata'),
	url(r'^showdata/$', views.showdata, name='showdata'),
]
