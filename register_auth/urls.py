from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'registration/$', views.registration, name='registration'),
]
