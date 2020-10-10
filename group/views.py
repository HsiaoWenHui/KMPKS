from django.shortcuts import render
from personal.models import UserProfile
from group.models import group,articleGroup,articleGroup_category,group_category,member,message
from article.models import article,tag
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt 
from django.db.models import Q
# Create your views here.
def allGroup(request):
    group_list=group.objects.all()
    user=UserProfile.objects.get(user=request.user)
    userGroup=member.objects.filter(memberID=user,state=0)#列使用者所在的所有群組
    applyingGroup=member.objects.filter(memberID=user,state=1)
    userGroup_list=[]
    applyingGroup_list=[]
    for i in userGroup:
        userGroup_list.append(i.groupID)
    for i in applyingGroup:
        applyingGroup_list.append(i.groupID)
    return render(request,"groups.html",locals())

def mygroups(request):
    user=UserProfile.objects.get(user=request.user)
    member_list=member.objects.filter(memberID=user)
    
    return render(request,"myGroups.html",locals())

def addGroup(request):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        group_list=member.objects.filter(memberID=user)
        
        if request.method =="POST":
            nTitle=request.POST['newTitle']
            nIntro=request.POST['newIntro']
            nPrivate=request.POST['newPrivate']
            nAnnounce=request.POST['newContent']
            nOwner=user

            g_unit=group.objects.create(name=nTitle,intro=nIntro,owner=nOwner,privacy=nPrivate,announcement=nAnnounce)
            g_unit.save()
            m_unit=member.objects.create(groupID=g_unit,memberID=user,state=0)
            m_unit.save()
            return HttpResponseRedirect('/group/'+str(g_unit.id))
        else:
           
            return render(request, 'add_group.html',locals())
    else:
        return HttpResponseRedirect('/accounts/login')


def groupIndex(request,group_id):
    g_unit=group.objects.get(id=group_id)
    user=UserProfile.objects.get(user=request.user)
    name=user.name
    article_list=articleGroup.objects.filter(groupID=g_unit) #群組內所有文章
    category_list=group_category.objects.filter(group=g_unit)#群組內所有分類
    article_category=articleGroup_category.objects.filter(categoryID__in=category_list)#群組內分類的文章關聯表
    msg=message.objects.filter(group=g_unit)
    
    if request.user.is_authenticated:
        
        if g_unit.privacy == 1:#在公開群組的情況下，使用者為該群組成員則state=0 否則為1
            member_list=member.objects.filter(groupID=g_unit) 
            a_member=len(member_list)
            a_article=len(article_list)
            
            for m in member_list:
                if m.memberID == user and m.state == 0: #如果使用者在成員列表中 且 已加入 則 state=0
                    state=0
                elif m.memberID == user and m.state == 1:#如果使用者在成員列表中 且 申請中 則 state=1
                    state=1
                else: #如果都沒有在列表中 則代表尚未申請加入群組 則 state=2
                    state=2
            return render(request, 'group.html',locals())
        else:
            member_list=member.objects.filter(groupID=g_unit,state=0) #0:已加入 1:申請中
            a_member=len(member_list)
            a_article=len(article_list)
            
            for m in member_list:
                if m.memberID == user:
                    return render(request, 'group.html',locals())
                else:
                    continue
            return HttpResponseRedirect('/group')
    else:
        return HttpResponseRedirect('/accounts/login')
@csrf_exempt
def editGroup(request,index):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user) #使用者
        e_group=group.objects.get(id=index) #欲編輯之群組
        gID=e_group.id

        article_list=articleGroup.objects.filter(groupID=e_group)
        member_list=member.objects.filter(groupID=e_group)
        category_list=group_category.objects.filter(group=e_group)#該群組的所有分類
        article_category_list=articleGroup_category.objects.filter(categoryID__in=category_list)#該群組中的文章及分類關係

        number=0
        article_count=0
        if user.id == e_group.owner.id:
            if  request.method=="POST":
                e_group.name=request.POST['newTitle']
                e_group.intro=request.POST['newIntro']
                e_group.privacy=request.POST['newPrivate']
                
                e_group.announcement=request.POST['newContent']
                e_group.save()

                return HttpResponseRedirect('/group/'+str(e_group.id))
            else:
                name=e_group.name
                intro=e_group.intro
                private=e_group.privacy
                announcement=e_group.announcement
                return render(request, 'edit_group.html',locals())
        else:
            return render(request, '/home',locals())
    else:
        return HttpResponseRedirect('/accounts/login')

def removeGroup(request,index):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        de_group=group.objects.get(id=index)
        member_list=member.objects.filter(groupID=de_group)
        article_list=articleGroup.objects.filter(groupID=de_group)
        print("呼叫刪除功能")
        if user.id == de_group.owner.id:
            for i in article_list:
                i.delete()
            for i in member_list:
                i.delete()
            de_group.delete()
            print("群組刪除")
            return HttpResponseRedirect('/group/mygroups/')
        else:
            print("沒刪到")
            return render(request, '/group/'+str(de_group.id))
    else:
        return HttpResponseRedirect('/accounts/login')

def joinGroup(request,index):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        apply_group=group.objects.get(id=index)
        application=member.objects.filter(groupID=apply_group,memberID=user)
        if not application:
            apply_member=member.objects.create(groupID=apply_group,memberID=user,state=1)
            apply_member.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #導向上一頁
    else:
        return HttpResponseRedirect('/accounts/login')

def cancelGroup(request,index):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        apply_group=group.objects.get(id=index)
        apply_member=member.objects.get(groupID=apply_group,memberID=user)
        if not apply_member:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            if(apply_member.state == 1):
                apply_member.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/login')

def allmembers(request,index):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        g_unit=group.objects.get(id=index)
        member_list=member.objects.filter(groupID=g_unit)
        number=0

        return render(request, 'all_members.html',locals())
    else:
        return HttpResponseRedirect('/accounts/login')

def addMember(request,groupIndex,memberIndex):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        applier=UserProfile.objects.get(id=memberIndex)
        g_unit=group.objects.get(id=groupIndex)
        application=member.objects.get(groupID=g_unit,memberID=applier)
        if(user==g_unit.owner and application.state==1):
            application.state=0
            application.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/login')

def leaveGroup(request,groupIndex,memberIndex):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        g_unit=group.objects.get(id=groupIndex)
        m_unit=UserProfile.objects.get(id=memberIndex)
        application=member.objects.get(groupID=g_unit,memberID=m_unit,state=0)
        if not application:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            application.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    else:
        return HttpResponseRedirect('/accounts/login')
@csrf_exempt
def addCategory(request,index):
    if request.user.is_authenticated:
        g_unit=group.objects.get(id=index)
        all_category=group_category.objects.filter(group=g_unit)
        all_category_list=[]
        for unit in all_category:
            all_category_list.append(unit.name)

        
        nCategory=request.POST['newCategory']
        cate_list=nCategory.split(',')
        for c in cate_list:
            if c not in all_category_list and c!="":
                newCate=group_category.objects.create(name=c,group=g_unit)
            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/login')

@csrf_exempt
def updateCategory(request,index):
    
    if request.user.is_authenticated:
        #取得群組的所有分類
        g_unit=group.objects.get(id=index)
        c_alllist=group_category.objects.filter(group=g_unit)

        #因為前端可以取得分類但是沒辦法直接和文章做連接，所以再從前端傳文章的ID
        articleIndex=request.POST.getlist('aIndex[]',None) #取得更新的文章ID
        number=len(articleIndex)

        #因為getlist不能直接存array list (newCate[]會沒東西，要newCate[0][])所以要一個一個拉進來
        category_list=[]
        for i in range(number):
            category_list.append(request.POST.getlist('newCate['+str(i)+'][]',None) )#取得文章的分類ID串列 例如:{["1"],["0","1"]....}
     
        #開始比對
        for i in range(len(articleIndex)):
            
            a_unit=article.objects.get(id=int(articleIndex[i])) #取文章
            #取得群組裡面特定文章的所有舊有分類
            c_old=articleGroup_category.objects.filter(categoryID__in=c_alllist).filter(articleID=a_unit)
            c_oldlist=[]#因為用ID做比對，所以要把後端找到的分類整理成ID串列 
            for unit in c_old:
                c_oldlist.append(unit.categoryID.id)
            
            #取文章對應的更新 分類ID 例如:["0","1"]
            c_newlist=category_list[i] 
            if len(c_newlist):#是空串列就不用新增了
               
                for c in c_newlist:#如果更新分類不在舊有的分類中則新增
                    if int(c) not in c_oldlist:
                        c_unit=group_category.objects.get(id=int(c))
                        ac_unit=articleGroup_category.objects.create(articleID=a_unit,categoryID=c_unit)
            else:#歸為未分類
                c_unit=group_category.objects.get(group=g_unit,name="未分類")
                ac_unit=articleGroup_category.objects.create(articleID=a_unit,categoryID=c_unit)

            for c in c_oldlist:#如果舊有的分類不在更新分類中代表該分類被移除
                if str(c) not in c_newlist:
                    c_unit=group_category.objects.get(id=c) 
                    ac_unit=articleGroup_category.objects.get(articleID=a_unit,categoryID=c_unit)
                    ac_unit.delete()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/login')

def delCategory(request,groupIndex,categoryIndex):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        g_unit=group.objects.get(id=groupIndex)
        c_unit=group_category.objects.get(id=categoryIndex)
        article_category=articleGroup_category.objects.filter(categoryID=c_unit)
        if user.id == g_unit.owner.id:
            if not article_category:
                c_unit.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                article_category.delete()
                c_unit.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/login')


def categories(request,groupID,categoryID):
    user=UserProfile.objects.get(user=request.user)
    cate_unit=group_category.objects.get(id=categoryID)
    cate_articles_rel=articleGroup_category.objects.filter(categoryID=cate_unit)
    cate_articles=[]
    for c in cate_articles_rel:
        cate_articles.append(c.articleID)
    
    return render(request, 'category.html',locals())




def delArticle(request,groupIndex,articleIndex):
    if request.user.is_authenticated:
        user=UserProfile.objects.get(user=request.user)
        g_unit=group.objects.get(id=groupIndex)
        a_unit=article.objects.get(id=articleIndex)
        
        article_group=articleGroup.objects.get(groupID=g_unit,articleID=a_unit) #取文章群組關聯
        category_list=group_category.objects.filter(group=g_unit)
        article_category=articleGroup_category.objects.filter(categoryID__in=category_list).filter(articleID=a_unit)
        if user.id == g_unit.owner.id:
            if not article_group:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                article_group.delete()
                article_category.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/accounts/login')


def chat(request,group_id):
    user=UserProfile.objects.get(user=request.user)
    name=user.name
    g_unit=group.objects.get(id=group_id)
    return render(request, 'chat.html',locals())

def search(request):
    if 'group_keyword' in request.GET:
        user=UserProfile.objects.get(user=request.user) 
        keyword=request.GET["group_keyword"]
        search_result=group.objects.filter(Q(name__contains=keyword)|Q(intro__contains=keyword))
        return render(request, 'group_search.html',locals())
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def article_search(request,index):
    if "group_article_keyword" in request.GET:
        user=UserProfile.objects.get(user=request.user)
        g_unit=group.objects.get(id=index)

        search_way=1#組內搜尋
    
        article_in_group=articleGroup.objects.filter(groupID=index)
        article_list=[]
        for i in article_in_group:
            article_list.append(i.articleID.id)
        keyword=request.GET["group_article_keyword"]
        try:
            tag_keyword=tag.objects.get(name=keyword)
        except:
            tag_keyword=None
        search_temp=article.objects.filter(id__in=article_list)
        search_temp=search_temp.filter(Q(tags=tag_keyword)|Q(title__contains=keyword)|Q(content__contains=keyword))
        search_result=search_temp.filter(Q(private=0)|Q(private=2))
        return render(request, 'search.html',locals())
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))