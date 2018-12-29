from .import views
from django.conf.urls import url

urlpatterns = [
    url(r'^upgoods/$', views.upgoods, name='upgoods'),
    url(r'^goodsinfo/$', views.goodsinfo, name='goodsinfo'),
    url(r'^updownGoods/$', views.updownGoods, name='updownGoods'),
    url(r'^updategoods/$', views.updategoods, name='updategoods'),
    url(r'^detailinfo/$', views.detailinfo, name='detailinfo'),
    url(r'^single/$', views.single, name='single'),

]