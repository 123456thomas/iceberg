from django.db import models
from store.models import stores
from users.models import Users
# Create your models here.


class goods(models.Model):
    id = models.AutoField(primary_key=True)
    waresname = models.CharField(max_length=30,verbose_name='商品名字')
    waresinfo = models.CharField(max_length=200,verbose_name='商品详情')
    waressize = models.CharField(max_length=4,verbose_name='商品尺码')
    waresstock = models.PositiveIntegerField(verbose_name='商品库存',default=0)
    warescount = models.PositiveIntegerField(verbose_name='商品销量',default=0)
    waresprice = models.FloatField(verbose_name='商品价格', max_length=7)
    borntime = models.DateTimeField(verbose_name='上架时间', auto_now_add=True)
    warestatus = models.BooleanField(verbose_name='商品状态',default=True)
    forgoo = models.ForeignKey(stores, on_delete=models.CASCADE)

class category(models.Model):
    id = models.AutoField(primary_key=True)
    category1 = models.CharField(max_length=20,verbose_name='男士/女士')
    category2 = models.CharField(max_length=20,verbose_name='季节')
    forcat = models.ForeignKey(goods, on_delete=models.CASCADE)

class goodsimgs(models.Model):
    id = models.AutoField(primary_key=True)
    imag0 = models.ImageField(upload_to='static/upload/goods', verbose_name='商品图片')
    forimg = models.ForeignKey(goods, on_delete=models.CASCADE)


# 收藏
class cllocter(models.Model):
    id = models.AutoField(primary_key=True)
    goodsid = models.IntegerField(verbose_name='商品id')
    forcll = models.ForeignKey(Users, on_delete=models.CASCADE)
