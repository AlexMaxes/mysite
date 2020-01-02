from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from . import models
from . import forms
import hashlib
import datetime


# Create your views here.

def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        # 若已登录
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        message = '是不是哪一项填错了？'
        # if username.strip() and password:
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '此用户并不存在'
                print(username, password, 'incorrect username')
                # return render(request, 'login/login.html',{'message':message})
                return render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                message = '你邮件还没确认吧？'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                print(username, password)
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                # request.session['set_time'] = user.c_time
                # request.session['pass']=user.password
                return redirect('/index/')
            else:
                message = '密码不对再想想?'
                print(username, password, 'incorrect password')
                # return render(request,'login/login.html',{'message':message})
                return render(request, 'login/login.html', locals())
        else:
            print('incorrect form or verification failed')
            # return render(request,'login/login.html',{'message':message})
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    # return render(request, 'login/login.html')
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "是不是哪填的格式不对？"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次密码咋输的不一样？'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '这名字别人用过了'
                    return render(request, 'login/register.html', locals())
                same_email = models.User.objects.filter(email=email)
                if same_email:
                    message = '这邮箱咋被别人注册过了？'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(username,email, code)
                request.session['mail_send'] = True
                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 若未登陆
        return redirect("/login/")
    request.session.flush()
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


def hash_code(s, salt='Alex'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(name, email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = 'Automatic registration confirmation email from ALEXMAXES'
    text_content = 'Just test content! There will be more in future!  And if you can see this,you can\'t get the emailcode, please contact the administrator '
    # text_content是用于当HTML内容无效时的替代txt文本
    html_content = '<p>Hi! {}!</p><p>Just test content! There will be more in future! And here is your ' \
                   '<a href="http://{}/confirm/?code={}" target=blank>Confirm link! </a>' \
                   'Click that to confirm your sign up! And that link is valid for {} days！</p>' \
                   '<p>welcome to my site:<a href="http://47.93.231.184" target=blank>www.wushuang.com</a>' \
                   '(There is empty, just for now :)</p> <p>AlexMaxes</p>'.format(name, '47.93.231.184', code,settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = 'NULL'
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '你这个请求无效噢'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '这个链接过期了吧，重新注册去'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '注册成功！！！马上跳转登陆页面~'
        request.session.flush()
        return render(request, 'login/confirm.html', locals())
