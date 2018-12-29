from django.db import models
import datetime

# Create your models here.
class Usersmanage(models.Manager):
    def Create_user(self, name, pwd, email):
        user = self.create(pickname=name, pwd=pwd, email=email)
        user.save()


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    pickname = models.CharField(max_length=20, verbose_name='昵称')
    pwd = models.CharField(max_length=50, verbose_name='密码')
    email = models.EmailField( verbose_name='邮箱')
    adress = models.CharField(max_length=100, blank=True, verbose_name='地址')
    phone = models.CharField(max_length=11,blank=True)
    catime = models.DateTimeField(verbose_name='注册时间', auto_now_add=True)
    header = models.ImageField(upload_to='static/upload/head', verbose_name='头像', default='static/upload/head/header.png')
    usermanage = Usersmanage()

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    adress = models.CharField(max_length=100, blank=True, verbose_name='地址')
    adfor = models.ForeignKey(Users, on_delete=models.CASCADE)