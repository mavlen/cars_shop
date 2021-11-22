from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils.crypto import get_random_string

from .models import Author, ConfirmCode
from .forms import LoginForm, RegisterForm,ResetPassword,NewPassword
from django.contrib.auth.forms import UserCreationForm
from .utils import send_register_mail


def register_view(request):
    form = RegisterForm(request.POST or None)
    message = "Потча уже занята"
    if request.method == 'POST':
        author =  Author.objects.filter(email=request.POST['email'])
        if author:
            if author[0].verified:
                return render(request, 'register.html', {'form': form, 'message':message}) 
            code = ConfirmCode.objects.create(customer=author[0])
            message = f"{settings.SITE_URL}authe/confirm/{code.code}/"
            send_register_mail(message,author[0].email)
            message = "Вам отправлена ссылка"
        if form.is_valid(): 
            user = form.save()
            code = ConfirmCode.objects.create(customer=user)
            message = f"{settings.SITE_URL}authe/confirm/{code.code}/"
            send_register_mail(message,user.email)
            message = "Вам отправлена ссылка"
        return render(request, 'register.html', {'form': form, 'message':message})
    return render(request, 'register.html', {'form': form})

def confirm_view(request, code):
    code = ConfirmCode.objects.filter(code = code)
    form = RegisterForm(None)
    message = 'Код не найден'
    if code:
        user = code[0].customer
        user.verified = True
        user.save()
        code.delete()
        message = 'Ваша почта потверждена'
    return render(request, 'register.html', {'message':message, 'form': form})

def login_view(request):
    form  = LoginForm(request.POST or None)
    message = 'логин или пароль не верный'
    if request.method == 'POST' and form.is_valid():
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            message = 'Все ок'
            login(request, user)
            return render(request, 'login.html', {'form':form, 'message':message})
    return render(request, 'login.html', {'form':form, 'message':message})

def logout_view(request):
    logout(request)
    return redirect('blog:post_list') 


def reset_password(request):
    form = ResetPassword(request.POST or None)
    message = ''
    if request.method == 'POST':
        author = Author.objects.filter(email=request.POST['email'])
        if author:
            code = ConfirmCode.objects.create(customer=author[0])
            msg = f"{settings.SITE_URL}authe/reset/{code.code}"
            send_register_mail(msg,author[0].email)
            message = 'Вам отправлена ссылка для сброса пароля'
            return render(request,'reset.html',{'form':form,'message':message})
        message = 'Такого пользователя нет'
        return render(request,'reset.html',{'form':form,'message':message})
    return render(request,'reset.html',{'form':form,'message':message})

def new_password(request, code):
    message = 'Неверный код'
    form = ResetPassword(request.POST or None)
    if ConfirmCode.objects.filter(code=code):
        code = ConfirmCode.objects.get(code=code)
        if not code.confirm:
            code.confirm = True
            code.save()
            new_password = get_random_string(length=6)
            code.customer.set_password(new_password)
            code.customer.save()
            send_register_mail(new_password,code.customer.email)
            return render (request, 'reset.html', {'form':form,'message': 'Ваш пароль выслан на почту'})
        return render(request, 'reset.html', {'form':form,'message': 'Ваш пароль уже сброшен'}) 
    return render(request, 'reset.html', {'form':form,'message':message}) 


def edit_password(request):
    form = NewPassword(request.POST or None)
    message = ''
    if request.user.is_authenticated and request.POST:
        if request.user.check_password(request.POST['old_password']):
            request.user.set_password(request.POST['new_password'])
            request.user.save()
            message = 'Пароль был изменен'
            return render(request,'new_password.html',{'form':form,'message':message})
        message = 'Старый пароль не верен'
        return render(request,'new_password.html',{'form':form,'message':message})
    return render(request,'new_password.html',{'form':form,'message':message})