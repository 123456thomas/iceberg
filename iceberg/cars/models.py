from django.db import models
from users.models import Users
from goods.models import goods
# Create your models here.

class Cars(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(verbose_name='购物车状态', default=True)
    forcar = models.ForeignKey(Users, on_delete=models.CASCADE)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    goodname = models.CharField(verbose_name='商品名', max_length=30)
    goodimg = models.CharField(verbose_name='商品图片', max_length=255)
    gooodsize = models.CharField(verbose_name='商品尺码', max_length=52,default='L')
    goodnum = models.IntegerField(verbose_name='数量')
    goodprice = models.FloatField(verbose_name='单价')
    goodid = models.IntegerField(verbose_name='商品id')
    forord = models.ForeignKey(Cars, on_delete=models.CASCADE)


class shoplist(models.Model):
    id = models.AutoField(primary_key=True)
    goodnumnam = models.CharField(verbose_name='商品', max_length=255)
    acount = models.FloatField(verbose_name='总额')
    forord = models.ForeignKey(Users, on_delete=models.CASCADE)



