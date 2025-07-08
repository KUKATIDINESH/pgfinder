from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
# Create your views here.


def user_login(request):
    context={}
    if request.method=='POST':
        user_name=request.POST.get('user_name')
        pw=request.POST.get('password')
        user=authenticate(request,username=user_name,password=pw)
        if user is not None:
            print('user')
            login(request,user)
            return redirect('home')
        context={'error':'Sorry username and password mis match not found'}
    return render(request,'login.html',context)
def signin(request):
    context={}
    if request.method=='POST':
        user_name=request.POST.get('user_name')
        pw1=request.POST.get('password1')
        pw2=request.POST.get('password2')
        em=request.POST.get('email')
        print(user_name,em,pw1,pw2)
        if pw1==pw2:
            print(pw1,pw2)
            if User.objects.filter(username=user_name).exists():
                context['error']="user name alreadu Existed"
            else:
                User.objects.create_user(username=user_name,password=pw1,email=em)
                return redirect('login')
        else:
            context['error']="password didn't matched"

    return render(request,'signup.html',context)
def user_logout(request):
    logout(request)
    return redirect('home')