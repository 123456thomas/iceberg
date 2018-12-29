from django.shortcuts import render, HttpResponse, redirect

# 导入事务模块
from django.db import transaction
from . import models


# 导入加密
import hashlib

# 邮箱验证
from django.conf import settings
from django.core.mail import send_mail

# 验证码导入模块
from io import BytesIO
from . import utils


# 用于序列化Django对象的接口
from django.core.serializers import serialize, deserialize


# 导入分页模块
from django.core.paginator import Paginator
from django.conf import settings


# 导入商品和商店类
from goods.models import goods
from store.models import stores

from cars.models import shoplist
# Create your views here.


# 主页
def index(request):
    # 判断session 是否含有goodsall
    if 'goodsall' not in request.session:
        stores2 = stores.objects.filter(states=True)
        stem =[]
        for i in stores2:
            stem.extend(goods.objects.filter(warestatus=True,forgoo=i))
        request.session['goodsall'] = stem
    # 分页
    pagesize = settings.PAGESIZE
    paginator = Paginator(request.session['goodsall'], pagesize)
    # 获取当前页的页码
    pagenum = request.GET.get('pagenum', default=1)
    page = paginator.page(int(pagenum))
    return render(request, 'index.html',{'paginator':paginator, 'page':page})




from random import Random


# 邮箱注册验证码
def em_code():
    # 生成随机字符串
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(8):
        str += chars[random.randint(0, length)]
    return str


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'users/register.html')
    elif request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        pickname = request.POST['pickname']
        email = request.POST['email']
        if password != confirm_password:
            return render(request, 'users/register.html', {'msg': "两次密码不一致"})
        user = models.Users.usermanage.filter(pickname=pickname)
        if user.exists():
            return render(request, 'users/register.html', {'msg': "该用户名已存在，请重新注册"})
        else:
            m_title = "iceberg冰山欢迎你，来吧!"
            m_msg = em_code()
            try:
                send_mail(m_title, m_msg, settings.EMAIL_FROM, [email])
            except Exception as e:
                print(e,66666)
            md = hashlib.md5()
            md.update(password.encode('utf8'))
            pwd = md.hexdigest()
            request.session['mailcode'] = m_msg
            request.session['pickname'] = pickname
            request.session['email'] = email
            request.session['pwd'] = pwd
            return render(request, 'users/email_active.html', {'msg': '激活码已发至你邮箱'})


# 激活，注册成功
def actives(request):
    if request.method == 'POST':
        # 防止重复激活
        try:
            if request.POST['emcode'] == request.session['mailcode']:
                # 添加新用户
                user = models.Users(pickname=request.session['pickname'], pwd=request.session['pwd'],
                                    email=request.session['email'])
                user.save()
                request.session.delete()
                return render(request, 'users/email_active.html', {'msg': '注册成功'})
            else:
                return render(request, 'users/email_active.html', {'msg': '验证码错误，请重试'})
        except:
            return render(request, 'users/email_active.html')
    else:
        return render(request, 'index.html')


# def reg_email(request):
#     m_title = "赵电商账号激活邮件"
#     m_msg = "点击激活您的账号"
#     send_mail(m_title, m_msg, settings.EMAIL_FROM, ['1304895886@qq.com'])
#     return render(request, "users/register.html", {"msg": "恭喜您，注册成功，请登录邮箱激活账号！！"})


# 生成验证码
def yanzheng(request):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = utils.create_code()
    # 保存验证码信息到 session 中，方便下次表单提交时进行验证操作
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


from django.forms.models import model_to_dict
# 用于序列化Django对象的接口
from django.core.serializers import serialize, deserialize

# 引入店类
from store.models import stores



# 登录
def logins(request):
    # 超链接访问
    if request.method == 'GET':
        return render(request, 'users/logins.html')
    elif request.method == 'POST':
        yanzh = request.session['check_code']
        if yanzh != request.POST["code"]:
            return render(request, 'users/logins.html', {'msg': '验证码错误'})
        username = request.POST['username']
        users = models.Users.usermanage.filter(pickname=username)
        if users.exists():
            user = users.first()
            pwds = request.POST['pwd']
            md = hashlib.md5()
            md.update(pwds.encode('utf8'))
            pwds = md.hexdigest()
            if user.pwd == pwds:
                request.session['user'] = user
                return redirect('users:index')
            else:
                msg = '密码错误'
        else:
            msg = '用户名不存在'
        return render(request, 'users/logins.html', {'msg': msg})



# 展示用户信息
def userinfor(request):
    # 判断有没有登陆
    if 'user' not in request.session:
        return redirect('users:logins')
    store1 = stores.objects.filter(masters=request.session['user'])
    if store1.exists():
        request.session['storelis'] = store1
    return render(request, 'users/userinfor.html')



# 完善会员信息
def updateuser(request):
    if request.method == 'GET':
        return render(request, 'users/updateuser.html')
    elif request.method == 'POST':
        phone = request.POST['phone']
        diqu = request.POST['diqu']
        province = request.POST['province']
        city = request.POST['city']
        qu = request.POST['qu']
        intro = request.POST['intro']
        address = diqu + province + city + qu + intro
        user = request.session['user']
        user.adress = address
        user.phone = phone
        try:
            header = request.FILES['header']
            user.header = header
        except:
            pass
        user.save()
        request.session['user'] = user

        request.session['storelis'] = stores.objects.filter(masters=user)
        return redirect('users:userinfor')


# 添加地址，并默认
def addaddress(request):
    if request.method == 'GET':
        return render(request,'users/addaddress.html')
    # 添加
    elif request.method == 'POST':
        diqu = request.POST['diqu']
        province = request.POST['province']
        city = request.POST['city']
        qu = request.POST['qu']
        intro = request.POST['intro']
        address = diqu + province + city + qu + intro
        user = request.session['user']
        temp = user.adress
        # 将新增地址设为默认地址
        user.adress = address
        user.save()
        address1 = models.Address(adfor=user, adress=temp)
        address1.save()
        # 判断有没有登陆
        if 'user' not in request.session:
            return redirect('users:logins')
        # 更新session
        request.session['user'] = user
        request.session['storelis'] = stores.objects.filter(masters=user)
        request.session['addresslis'] = models.Address.objects.filter(adfor=user)
        return redirect('cars:myorder')


# 改为默认地址
def updateaddre(request):
    newaddr = models.Address.objects.get(id=int(request.GET['sid']))
    user = request.session['user']
    temp = user.adress
    print(temp)
    user.adress = newaddr.adress
    user.save()
    newaddr.adress = temp
    newaddr.save()
    request.session['user'] = user
    request.session['addresslis'] = models.Address.objects.filter(adfor=user)
    return redirect('cars:myorder')


# 修改基本信息
def baseinfo(request):
    if request.method == 'GET':
        return render(request, 'users/baseinfo.html')
    elif request.method == 'POST':
        pickname = request.POST['pickname']
        email = request.POST['email']
        oripassword = request.POST['oripassword']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'users/baseinfo.html', {'msg': '两次输入新密码不一致'})
        md = hashlib.md5()
        md.update(oripassword.encode('utf8'))
        pwds = md.hexdigest()
        user = request.session['user']
        if user.pwd == pwds :
            user.pickname=pickname
            user.email=email
            if password1 != '':
                md = hashlib.md5()
                md.update(password1.encode('utf8'))
                pwds1 = md.hexdigest()
                user.pwd = pwds1
            user.save()
            request.session['user']=user
            return redirect('users:userinfor')
        else:
            return render(request, 'users/baseinfo.html', {'msg': '密码错误'})


# 开店
def createstore(request):
    # 验证登陆
    if 'user' not in request.session:
        return redirect('users:logins')
    if request.method == 'GET':
        user = request.session['user']
        print(type(user.phone))
        if user.adress == '' or user.phone == '':
            return render(request, 'users/userinfor.html', {'msg': '请先完善个人信息'})
        else:
            return render(request, 'users/createstore.html')
    elif request.method == 'POST':
        storename = request.POST['storename']
        storeimg = request.FILES['storeimg']
        info = request.POST['info']
        store1 = stores(storename=storename, storeinfo=info, storephoto=storeimg, masters=request.session['user'])
        store1.save()
        store2 = stores.objects.filter(masters=request.session['user'])
        request.session['storelis'] = store2
        return render(request, 'users/userinfor.html', {'msg': '您好没上架商品，去您的店铺看看吧'})


# 推出
def quite(request):
    request.session.delete()
    return redirect('users:index')

def ordered(request):
    # 判断有没有登陆
    if 'user' not in request.session:
        return redirect('users:logins')
    ordered = shoplist.objects.filter(forord=request.session['user'])
    return render(request, 'users/ordered.html', {'ordered': ordered})

