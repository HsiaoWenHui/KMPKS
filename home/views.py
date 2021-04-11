from django.shortcuts import render,HttpResponse
from django.contrib import auth
from django.http import HttpResponseRedirect
from group.models import group
from article.models import article,tag
from bs4 import BeautifulSoup
import random
from django.db.models.aggregates import Count
from personal.models import UserProfile
from django.contrib.auth.models import User
import csv
def index(request):
    # with open('member_2.csv', mode='r') as csv_file:
            
    #         reader = csv.reader(csv_file)
    #         for line in reader:
    #             if line is not None:
                    
    #                 name = line[0]
    #                 username = line[1]
    #                 password = line[2]
    #                 email=username
                    
    #                 try:
    #                     user=User.objects.get(username=username)
    #                 except:
    #                     user=None
                
    #                 if user!=None:
    #                     continue
    #                 else:
    #                     newUser=User.objects.create_user(username,username,password)
    #                     newUser.save()
    #                     unit=UserProfile.objects.create(user=newUser,name=name,intro="")
    #                     unit.save()
    return render(request, 'home/index.html',locals())

#維護
def maintenance(request):
    return render(request, 'home/maintenance.html',locals())

# def home(request):
#     if request.user.is_authenticated:
#         user=UserProfile.objects.get(user=request.user)
#         total_user=UserProfile.objects.all()
#         total_article=article.objects.all()
#         total_group=group.objects.all().count()
#         popuPost_list=article.objects.filter(private=0).order_by('-like')[:4]
#         recentPost_list=article.objects.filter(private=0).order_by('-pubtime')[:4]
#         #找最新文章和最受歡迎文章
#         img_list=getImg(recentPost_list)
#         plainTex_list=getContentText(recentPost_list)
        
#         #找最受歡迎的TAG，參考https://blog.csdn.net/qq_25046261/article/details/79178462
#         tag_list = tag.objects.annotate(num_posts=Count('article')).order_by("-num_posts")[:4]
#         tag0=getAritcle(tag_list[0])
#         tag1=getAritcle(tag_list[1])
#         tag2=getAritcle(tag_list[2])
#         tag3=getAritcle(tag_list[3])
        
                
#         t_a_img_list_0=getImg(tag0)
#         t_a_img_list_1=getImg(tag1)
#         t_a_img_list_2=getImg(tag2)
#         t_a_img_list_3=getImg(tag3)

#         return render(request, 'home/home.html',locals())
#     else:
#         return HttpResponseRedirect('/accounts/login')
def home(request):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
 
    else:
        user=None

    total_user=UserProfile.objects.all()
    total_article=article.objects.all()
    total_group=group.objects.all().count()
    popuPost_list=article.objects.filter(private=0).order_by('-like')[:4]
    recentPost_list=article.objects.filter(private=0).order_by('-pubtime')[:4]
    #找最新文章和最受歡迎文章
    img_list=getImg(recentPost_list)
    plainTex_list=getContentText(recentPost_list)
        
    #找最受歡迎的TAG，參考https://blog.csdn.net/qq_25046261/article/details/79178462
    tag_list = tag.objects.exclude(name="").annotate(num_posts=Count('article')).order_by("-num_posts")[:4]
    
    tag0=getAritcle(tag_list[0])
    tag1=getAritcle(tag_list[1])
    tag2=getAritcle(tag_list[2])
    tag3=getAritcle(tag_list[3])
        
                
    t_a_img_list_0=getImg(tag0)
    t_a_img_list_1=getImg(tag1)
    t_a_img_list_2=getImg(tag2)
    t_a_img_list_3=getImg(tag3)    
    return render(request, 'home/home.html',locals())





def getAritcle(tag):
    tag_list=[]
    temp=article.objects.filter(tags=tag).order_by('-like')[:3]
    for a in temp:
        tag_list.append(a)
    return tag_list
def getImg(img):
    img_list=[]
    if not img:
        index=random.randint(1,3)
        img_list.append('/static/img/default'+str(index)+'.jpg/')
    else:
        for u in img:
            if 'img' in u.content:
                soup = BeautifulSoup(u.content, 'html.parser')
                img_tags = soup.find('img')
                for i in soup.select('img'):
                    i.extract()
                img_list.append(img_tags.get('src'))
            else:
                index=random.randint(1,3)
                img_list.append('/static/img/default'+str(index)+'.jpg/')

    return img_list

def getContentText(c):
    text_list=[]
    for u in c:
        soup = BeautifulSoup(u.content, 'html.parser')
        for i in soup.select('img'):
            i.extract()
        text_list.append(soup.prettify())
    return text_list

def faq(request):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        
    else:
        user=None
    return render(request, 'home/FAQ.html',locals())