from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^secret$', views.secret),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^createsecret$', views.createsecret),
    url(r'^logout$', views.logout),
    url(r'^like/(?P<message_id>\d+)$', views.like),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^popular$', views.popular),
]
