from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from . import models
from goods.models import goodsimgs,goods
from users.models import Address
# Create your views here.
# 必须登录


# 将商品添加到购物车，用户要先登录
def addCar(request):
    # 判断有没有登陆
    if 'user' not in request.session:
        return redirect('users:logins')
    if request.method == 'POST':
        car1 = models.Cars.objects.filter(forcar=request.session['user'],status=True)
        if car1.exists():
            car1 = car1.first()
        else:
            car1 = models.Cars(forcar=request.session['user'])
            car1.save()
        ware1 = request.session['addgoods']
        imgs = goodsimgs.objects.filter(forimg=ware1).first().imag0
        print(imgs,type(imgs))
        orders = models.Orders(goodname=ware1.waresname,
                        gooodsize=request.POST['waressize'],
                        goodimg=imgs,
                        goodid=ware1.id,
                        goodnum=int(request.POST['amount']),
                        goodprice=ware1.waresprice,
                        forord=car1)
        orders.save()
        return render(request,'goods/single.html',{'msg':'已加入购物车'})


# 购物车展示,必须先登录
def carorder(request):
    # 判断用户有没有登录
    try:
        if request.session['user'] is not None:
            pass
    except:
        return redirect('users:logins')
    # 后续待存入缓存
    request.session['cars'] = models.Cars.objects.filter(forcar=request.session['user'], status=True)
    sumcount = 0
    # 判断是否有购物车存在
    if request.session['cars'].exists():
        request.session['carsgood1'] = models.Orders.objects.filter(forord=request.session['cars'].first())
        for i in request.session['carsgood1']:
            sumcount += i.goodnum * i.goodprice
    else:
        request.session['carsgood1']=[]
    return render(request, 'cars/carorder.html', {'sumcount': sumcount})



# 更新购物车
def updatelist(request):
    subs = request.GET['del']
    num = request.GET['count']
    sid = int(request.GET['sid'])
    order2 = models.Orders.objects.get(id=sid)
    # 修改订单
    if subs =='0':
        order2.goodnum = num
        order2.save()
    # 删除订单
    elif subs =='1':
        order2.delete()
    return redirect('cars:carorder')


# 提交订单，查看购物清单
def myorder(request):
    if request.method == 'GET':
        user = request.session['user']
        if user.adress =='' or user.phone == '':
            return render(request, 'users/updateuser.html',{'msg':'请完善个人信息'})
        # 查看地址列表
        addresslis = Address.objects.filter(adfor=user)
        request.session['addresslis'] = addresslis
        # 计算总额
        sumcount = 0
        for i in request.session['carsgood1']:
            sumcount += i.goodnum * i.goodprice
        return render(request, 'cars/myorder.html',{'sumcount':sumcount})

def paysgoods(request):
    msg = '结算成功，等待商家已发货，请注意查收'
    mamlist = ''
    sumcount= 0
    for i in request.session['carsgood1']:
        wares1 = goods.objects.get(id=i.goodid)
        wares1.waresstock -= i.goodnum
        wares1.warescount += i.goodnum
        wares1.save()
        sumcount += i.goodnum * i.goodprice
        mamlist += i.goodname + '*' + str(i.goodnum)
    shoplist = models.shoplist(goodnumnam=mamlist, acount=sumcount,forord=request.session['user'])
    shoplist.save()
    # 清空购物车
    sid = request.session['carsgood1'].first().forord_id
    cars1 = models.Cars.objects.get(id=sid)
    cars1.status = False
    cars1.save()
    request.session['cars'] = models.Cars.objects.filter(forcar=request.session['user'], status=True)
    return render(request, 'cars/paysgoods.html',{'sumcount':sumcount})


