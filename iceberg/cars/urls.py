
from .import views
from django.conf.urls import url

urlpatterns = [
        url(r'^addCar/$', views.addCar, name='addCar'),
        url(r'^carorder/$', views.carorder, name='carorder'),
        url(r'^updatelist/$', views.updatelist, name='updatelist'),
        url(r'^myorder/$', views.myorder, name='myorder'),
        url(r'^paysgoods/$', views.paysgoods, name='paysgoods'),
    ]