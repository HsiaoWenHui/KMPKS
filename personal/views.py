from django.shortcuts import render
from django.http import HttpResponseRedirect
from personal.models import UserProfile
from article.models import article,category
from django.contrib import auth
from group.models import group,articleGroup,member
import random
from bs4 import BeautifulSoup
# Create your views here.
def personalIndex(request,index):
    if request.user.is_authenticated:
        owner=UserProfile.objects.get(id=index)
        user=UserProfile.objects.get(user=request.user)
        categories=category.objects.filter(creater=owner)
        name=owner.name
        intro=owner.intro
        member_list=member.objects.filter(memberID=user)
        article_list=article.objects.filter(author=owner.id)
        article_amount=len(article_list)
        
      
        return render(request, 'personal.html',locals())
    else:
        return HttpResponseRedirect('/accounts/login')

def editProfile(request):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        
        if  request.method=="POST":
            nName=request.POST['newName']
            user.name=nName
            request.user.email=request.POST['newEmail']
            #request.user.password=request.POST['newPassword']
            user.intro=request.POST['newIntro']
            user.save()
            request.user.save()
            auth.login(request,request.user)
            return HttpResponseRedirect('/personal/'+str(user.id))
        else:
            name=user.name
            email=request.user.email
            intro=user.intro
            return render(request, 'editProfile.html',locals())
    else:
        return HttpResponseRedirect('/accounts/login')





