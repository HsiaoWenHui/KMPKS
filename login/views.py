from django.shortcuts import render

# Create your views here.
"""
username	使用者的帳號，由字母、數字和底線組成
is_anonymous	是否是匿名用戶，永遠回傳False，若為AnonymousUser物件，則永遠回傳True
is_authenticated	用戶是否認證過，永遠回傳True，若為AnonymousUser物件，則永遠回傳False
first_name	名字
last_name	姓氏
email	電子郵箱
password	加密(經編碼)過後的密碼
is_staff	真假值，若為True，該用戶可登入admin後端
is_active	真假值，若為True，該用戶可登入
is_superuser	真假值，若為True，該用戶擁有全權限
last_login	用戶上一次登入的日期與時間
date_joined	用戶被創建的日期與時間

"""
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.models import User
from personal.models import UserProfile

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

def login(request):
    if request.user.is_authenticated:
        return render(request, 'home/home.html')
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/home')
        else:
            messages.error(request, 'Username or password is wrong!!')  
    return render(request,"registration/login.html",locals())

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def register(request):
    if request.method=="POST":
        # newUsername=request.POST['username']
        newPassword=request.POST['password']
        newEmail=request.POST['email']
        newUsername=newEmail.split("@")[0]

        # newName=request.POST['name']
        try:
            user=User.objects.get(username=newEmail)
        except:
            user=None
        
        if user!=None:
            messages.error(request, 'Email had been used!!')  
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            newUser=User.objects.create_user(newEmail,newEmail,newPassword)
            newUser.save()
            auth.login(request,newUser)
            unit=UserProfile.objects.create(user=newUser,name=newUsername,intro="")
            unit.save()
            
            return HttpResponseRedirect('/home/')

    else:
        return render(request, 'registration/regis.html')

def change_password(request):
    # if request.method == 'POST':
    #     form = PasswordChangeForm(request.user, request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user)  # Important!
    #         messages.success(request, 'Your password was successfully updated!')
    #         return redirect('change_password')
    #     else:
    #         messages.error(request, 'Please correct the error below.')
    # else:
    #     form = PasswordChangeForm(request.user)
    # return render(request, 'registration/change_password.html', {
    #     'form': form
    # })
    if request.user.is_authenticated:
        if request.method == 'POST':
            user=User.objects.get(username=request.user.username)
            if user.check_password(request.POST['old_password']):
                user.set_password(request.POST['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Your old password was incorrect.')
            return render(request, 'registration/change_password.html')
        else:
            return render(request, 'registration/change_password.html')
    else:
        return HttpResponseRedirect('/accounts/login')