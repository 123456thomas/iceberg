from django.db import models
from users.models import Users

# Create your models here.

class stores(models.Model):
    id = models.AutoField(primary_key=True)
    storename = models.CharField(max_length=20)
    storephoto = models.ImageField(upload_to='static/upload/store', validators='店铺图片', blank=True)
    reg_time = models.DateTimeField(verbose_name='营业时间', auto_now_add=True)
    storeinfo = models.CharField(max_length=100, blank=True)
    states = models.BooleanField(verbose_name='营业状态:', default=False)
    masters = models.ForeignKey(Users, on_delete=models.CASCADE)







