from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logoff$', views.logoff),
	url(r'^appointments$', views.appointments),
	url(r'^appointments/new$', views.create),
	url(r'^appointments/(?P<id>\d+)$', views.edit),
	url(r'^appointments/(?P<id>\d+)/update$', views.update),
	url(r'^appointments/(?P<id>\d+)/delete$', views.delete),
]