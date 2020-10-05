from django.shortcuts import render,HttpResponse
from django.contrib import auth
from django.http import HttpResponseRedirect
from personal.models import UserProfile
from article.models import article,tag
from group.models import member
from django.db.models.aggregates import Count
def getHotKeyword(request):
    tag_list = tag.objects.annotate(num_posts=Count('article')).order_by("-num_posts")[:10]
    group_list=member.objects.annotate(num_member=Count('groupID')).order_by("-num_member")[:10]

    return {
        'hot_tag': tag_list,
        'hot_group':group_list
    }