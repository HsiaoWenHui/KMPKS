from django.shortcuts import render,HttpResponse
from django.contrib import auth
from django.http import HttpResponseRedirect
from personal.models import UserProfile
from article.models import article,tag
from group.models import member,group
from django.db.models.aggregates import Count
def getHotKeyword(request):
    tag_list = tag.objects.annotate(num_posts=Count('article')).order_by("-num_posts")[:10]
    member_list=member.objects.values("groupID__id").annotate(Count('memberID'))
    group_list=[]
    for i in member_list:
        g=group.objects.get(id=i.get('groupID__id'))
        if g.privacy == 1:
            group_list.append(g)
    return {
        'hot_tag': tag_list,
        'hot_group':group_list
    }