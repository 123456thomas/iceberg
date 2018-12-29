from .import views
from django.conf.urls import url

urlpatterns = [
    url(r'^women/$', views.women, name='women'),
    url(r'^men/$', views.men, name='men'),
    url(r'^collection/$', views.collection, name='collection'),
    url(r'^(?P<id>\d+)/addcollect/$', views.addcollect, name='addcollect'),
    url(r'^colldel/$', views.colldel, name='colldel'),
    url(r"^mystore/$", views.mystore, name="mystore"),
    url(r"^updatestore/$", views.updatestore, name="updatestore"),

]