from django.conf.urls import patterns, url

from Respond import views

urlpatterns = patterns('',
    url(r'^$', views.giveJson),
)