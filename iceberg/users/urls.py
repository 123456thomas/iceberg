from .import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logins/$', views.logins, name='logins'),
    url(r"^active/$", views.actives, name="active"),
    url(r"^yanzheng/$", views.yanzheng, name="yanzheng"),
    url(r"^userinfor/$", views.userinfor, name="userinfor"),
    url(r"^updateuser/$", views.updateuser, name="updateuser"),
    url(r"^baseinfo/$", views.baseinfo, name="baseinfo"),
    url(r"^createstore/$", views.createstore, name="createstore"),
    url(r"^addaddress/$", views.addaddress, name="addaddress"),
    url(r"^updateaddre/$", views.updateaddre, name="updateaddre"),
    url(r"^ordered/$", views.ordered, name="ordered"),
    url(r"^quite/$", views.quite, name="quite"),
]