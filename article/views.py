from django.shortcuts import render
from article.models import article,tag,category,comment
from personal.models import UserProfile
from group.models import member,articleGroup,group
from django.http import HttpResponseRedirect,HttpResponse
# from markdownx.views import MarkdownifyView
from django import forms
from django.views import generic
# from simditor.fields import RichTextFormField
from django.views.generic.base import View
from django.views.generic.edit import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import random
from bs4 import BeautifulSoup
from django.contrib import messages
# from django.utils.module_loading import import_string
# from markdownx.settings import MARKDOWNX_MARKDOWNIFY_FUNCTION
# Create your views here.

# class articleView(View):
#     template_name = "article.html"
#     #override

#     def get(self, request, index):
#         user=UserProfile.objects.get(user=request.user)
#         a_unit=article.objects.get(id=index)
#         u_unit=UserProfile.objects.get(id=a_unit.author.id)
#         tags=a_unit.tags.all()
#         categories=a_unit.categorys.all()
#         return render(request, 'article.html',locals())


def articleIndex(request,index):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        a_unit=article.objects.get(id=index)
        
        u_unit=UserProfile.objects.get(id=a_unit.author.id)
        tags=a_unit.tags.all()
        categories=a_unit.categorys.all()
        privacy=a_unit.private ##文章隱私設定: 0:公開 1:私有 2:只有群組成員可以看
        comments=comment.objects.filter(post=a_unit)
        comment_count=comment.objects.filter(post=a_unit).count
        can_read=False

        if a_unit.author == user:
            can_read=True
        elif privacy==0:
            can_read=True
        elif privacy==2:
            joined_group=articleGroup.objects.filter(articleID=a_unit) #找出該文章所分享進去的群組
            joined_group_list=[]
            for i in joined_group:
                joined_group_list.append(i.groupID)
            permission_member = member.objects.filter(groupID__in=joined_group_list) #找出那些群組的成員關聯表
            if permission_member.filter(memberID=user): #如果使用者有在那些關聯表中 即可觀看文章
                can_read=True
            
        if can_read ==True:
            if request.method =="GET":
                a_unit.like=a_unit.like+0.5
                a_unit.save()
                return render(request, 'article.html',locals())
            if request.method =="POST":

                if 'message' in request.POST.keys() and request.POST['message']:
                    message=request.POST['message']
                    unit=comment.objects.create(post=a_unit,parent_id=0,created_by=user,content=message)
                    unit.save()
                else:
                    if 'replyTxt' in request.POST.keys() and request.POST['replyTxt']:
                        reply=request.POST['replyTxt']
                        p_id=request.POST['parent']
                        unit=comment.objects.create(post=a_unit,parent_id=p_id,created_by=user,content=reply)
                        unit.save()
                return render(request, 'article.html',locals())
        else:
            messages.error(request, '你沒有權限閱讀此文章哦') 
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/login')
def del_comment(request,index,comment_id):
    if request.user.is_authenticated:
        message=comment.objects.get(id=comment_id)
        user=UserProfile.objects.get(user=request.user)
        a_unit=article.objects.get(id=index)
        if a_unit.author == user:
            if message.parent_id==0:
                children_list=comment.objects.filter(parent_id=message.id)
                if(children_list):
                    for i in children_list:
                        i.delete()
                message.delete()
            else:
                message.delete()
                

    return HttpResponseRedirect('/article/'+str(a_unit.id))


def addArticle(request):
        if request.user.is_authenticated:
            
            user=UserProfile.objects.get(user=request.user)
            group_list=member.objects.filter(memberID=user,state=0)
            category_list=category.objects.filter(creater=user)
            if request.method =="POST":
                nTitle=request.POST['newTitle']
                nPrivate=request.POST['newPrivate']
                nContent=request.POST['newContent']
                nTags=request.POST['newTags']
                nCategory=request.POST['newCategory']
                oldCategory_list=request.POST.getlist('oldCategory',None)
                nAuthor=user
                nimg=getImg(request.POST['newContent'])
                unit=article.objects.create(title=nTitle,private=nPrivate,content=nContent,author=nAuthor,img=nimg)
                unit.save()

                addTags(unit.id,nTags)
                addCategory(unit,nCategory,oldCategory_list)
                #文章設定群組分享
                newGroup_list=request.POST.getlist('checkboxs',None)
                
                if newGroup_list :
                    for gID in newGroup_list:
                        g=group.objects.get(id=gID)
                        articleGroup_unit=articleGroup.objects.create(groupID=g,articleID=unit)
                        articleGroup_unit.save()
                        post=article.objects.get(id=unit.id)
                        if post.private==1:
                            post.private=2#防止有隱私設定私人 但是卻選要分享的群組
                            post.save()
                return HttpResponseRedirect('/article/'+str(unit.id)+'/')
                
            else:
            
                return render(request, 'add_article.html',locals())
        else:
            return HttpResponseRedirect('/accounts/login')

def editArticle(request,index):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        e_article=article.objects.get(id=index)
        group_list=member.objects.filter(memberID=user,state=0) #作者所在的所有群組成員關係表
        articleGroup_rel_list=articleGroup.objects.filter(articleID=e_article) #文章所在的所有群組文章關係表
        articleGroup_list=[]#存該文章所在的群組ID
        category_list=category.objects.filter(creater=user)#該作者的所有分類
        categories=e_article.categorys.all()
        for i in articleGroup_rel_list:
            articleGroup_list.append(i.groupID.id)
      
        if user.id == e_article.author.id:
            if  request.method=="POST":
                e_article.title=request.POST['newTitle']
                e_article.private=request.POST['newPrivate']
                e_article.content=request.POST['newContent']
                editTags(e_article,request.POST['newTags'])
                editCategory(e_article,request.POST['newCategory'],request.POST.getlist('oldCategory',None))
                e_article.img=getImg(request.POST['newContent'])
                e_article.save()

                newGroup_list=request.POST.getlist('checkboxs',None)#編輯過後的所有群組ID
                newGroup_list=[ int(x) for x in newGroup_list ] #把str轉int

                if newGroup_list: #防止有隱私設定私人 但是卻選要分享的群組
                    post=article.objects.get(id=index)
                    if post.private==1:
                        post.private=2#防止有隱私設定私人 但是卻選要分享的群組
                        post.save()

                for gID in newGroup_list:
                    if gID not in articleGroup_list:
                        g=group.objects.get(id=gID)
                        articleGroup_unit=articleGroup.objects.create(groupID=g,articleID=e_article)
                        articleGroup_unit.save()
                for delID in articleGroup_list:
                    if delID not in newGroup_list:
                        delUnit=group.objects.get(id=delID)
                        del_rel=articleGroup.objects.filter(groupID=delUnit,articleID=e_article)
                        del_rel.delete()
                
                return HttpResponseRedirect('/article/'+str(e_article.id))
            else:
                title=e_article.title
                private=e_article.private
                content=e_article.content
                tags=e_article.tags.all()
                aID=e_article.id
                return render(request, 'edit_article.html',locals())
        else:
            return render(request, '/home',locals())
    else:
        return HttpResponseRedirect('/accounts/login')

def removeArticle(request,index):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        de_article=article.objects.get(id=index)
        group_list=articleGroup.objects.filter(articleID=de_article)
        print("呼叫刪除功能")
        if user.id == de_article.author.id:
            for i in group_list:
                i.delete()
            de_article.delete()
            print("文章刪除")
            return HttpResponseRedirect('/personal')
        else:
            print("沒刪到")
            return render(request, '/article/'+str(de_article.id))
    else:
        return HttpResponseRedirect('/accounts/login')

def addTags(aID,tags):
    #抓此文章
    a=article.objects.get(id=aID)
    #把原有標籤抓出來
    all_tags=tag.objects.all()
    all_tags_list=[]
    for unit in all_tags:
        all_tags_list.append(unit.name)
    
    #處理文章標籤
    tag_list=tags.split(',')
    for t in tag_list:
        if t not in all_tags_list:
            newTag=tag.objects.create(name=t)
            a.tags.add(newTag)
        else:
            oldTag=tag.objects.get(name=t)
            a.tags.add(oldTag)

def addCategory(a,c,o):
    #把作者有的分類抓出來
    all_category=category.objects.filter(creater=a.author)
    all_category_list=[]

    for unit in all_category:
        all_category_list.append(unit.name)

    cate_list=c.split(',')
    for c in cate_list:
        if c not in all_category_list and c!="":
            newCate=category.objects.create(name=c,creater=a.author)
            a.categorys.add(newCate)
        elif c=="":
            try:
                oldCate=category.objects.get(name="未分類",creater=a.author)
                a.categorys.add(oldCate)
            except:
                newCate=category.objects.create(name="未分類",creater=a.author)
                a.categorys.add(newCate)
        else:
            oldCate=category.objects.get(name=c,creater=a.author)
            a.categorys.add(oldCate)
    
    for c in o:
        oldCate=category.objects.get(id = int(c))
        a.categorys.add(oldCate)

def editTags(a,tags):
    #把所有標籤抓出來
    all_tags=tag.objects.all()
    all_tags_list=[]
    for unit in all_tags:
        all_tags_list.append(unit.name)
    
    #把文章原本的標籤抓出來
    article_tags=a.tags.all()
    article_tags_list=[]
    for unit in article_tags:
        article_tags_list.append(unit.name)
    
    #編輯後的標籤
    tag_list=tags.split(',')

    #更新文章新增的標籤
    for t in tag_list:
        if t not in all_tags_list:
            newTag=tag.objects.create(name=t)
            a.tags.add(newTag)
        else:
            if t not in article_tags_list:
                newTag=tag.objects.get(name=t)
                a.tags.add(newTag)
    
    #更新文章刪除的標籤
    for t in article_tags_list:
        if t not in tag_list: #代表t被刪掉了
            delete_tag=tag.objects.get(name=t)
            a.tags.remove(delete_tag) #remove只刪除關係
    
    a.save()
              
def editCategory(a,c,o):
    #文章有的分類
    article_category=a.categorys.all()
    #把作者有的分類抓出來
    all_category=category.objects.filter(creater=a.author)
    all_category_list=[]
    for unit in all_category:
        all_category_list.append(unit.name)

    
    cate_list=c.split(',')
    

    for c in o:#檢查舊有分類
        oldCate=category.objects.get(id = int(c))
        if oldCate not in article_category:
            a.categorys.add(oldCate)
    for c in article_category:
        if(str(c.id) not in o):
            a.categorys.remove(c)
    for c in cate_list: #檢查新增分類
        if c not in all_category_list and c!="":
            newCate=category.objects.create(name=c,creater=a.author)
            a.categorys.add(newCate)
    
    a.save()
    
def tags(request,index):
    user=UserProfile.objects.get(user=request.user)
    tag_unit=tag.objects.get(id=index)
    tag_articles=article.objects.filter(tags=tag_unit,private=0)

    return render(request, 'tags.html',locals())

def categories(request,index):
    user=UserProfile.objects.get(user=request.user)
    cate_unit=category.objects.get(id=index)
    cate_articles=article.objects.filter(categorys=cate_unit,private=0)

    return render(request, 'category.html',locals())



def getImg(img):
    img_list=[]
    if not img:
        index=random.randint(1,3)
        img_list.append('/static/img/default'+str(index)+'.jpg/')
    else:
        
        if 'img' in img:
            soup = BeautifulSoup(img, 'html.parser')
            img_tags = soup.find('img')
            for i in soup.select('img'):
                i.extract()
            img_list.append(img_tags.get('src'))
        else:
            index=random.randint(1,3)
            img_list.append('/static/img/default'+str(index)+'.jpg/')

    return img_list[0]

def search(request):
    if "article_keyword" in request.GET:
        user=UserProfile.objects.get(user=request.user)
        search_way=0 #指所有文章搜尋
        keyword=request.GET["article_keyword"]
        try:
            tag_keyword=tag.objects.get(name=keyword)
        except:
            tag_keyword=None
        search_temp=article.objects.filter(Q(tags=tag_keyword)|Q(title__icontains=keyword)|Q(content__icontains=keyword)|Q(author__name__icontains=keyword))
        search_result=search_temp.filter(private=0)
        return render(request, 'search.html',locals())
        
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def all(request):
    user=UserProfile.objects.get(user=request.user)
    search_result=article.objects.filter(private=0).order_by('-pubtime')
    search_way=2 #指所有文章
    return render(request, 'search.html',locals())