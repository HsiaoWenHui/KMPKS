from django.db import models
from personal.models import UserProfile
from article.models import article
from django.utils import timezone
# Create your models here.
class group(models.Model):
    name=models.CharField(max_length=20,null=False)
    intro=models.TextField(null= False)
    owner=models.ForeignKey("personal.UserProfile",on_delete=models.CASCADE) 
    createTime=models.DateTimeField(auto_now_add= True)
    announcement=models.TextField(null=True)
    privacy=models.IntegerField(default=0)#1:公開 #0:非公開
    def __str__(self):
        return 'Group: '+self.name

class member(models.Model):
    groupID=models.ForeignKey("group",on_delete=models.DO_NOTHING)
    memberID=models.ForeignKey("personal.UserProfile",on_delete=models.CASCADE)
    state=models.IntegerField(default=1)#0:已加入 1:申請中
    # def __str__(self):
    #     return self.groupID + ' and ' + self.memberID


class group_category(models.Model):
    name = models.CharField(max_length=100,default="未分類")
    group=models.ForeignKey("group",on_delete=models.CASCADE,null=True)
    class Meta:
        unique_together = ('name', 'group',)
    def __str__(self):
        return 'category:'+ self.name+' group: '+self.group.name
class articleGroup_category(models.Model):
    articleID=models.ForeignKey("article.article",on_delete=models.CASCADE)
    categoryID=models.ForeignKey("group_category",on_delete=models.CASCADE)
    class Meta:
        unique_together = ('articleID', 'categoryID',)
class articleGroup(models.Model):
    articleID=models.ForeignKey("article.article",on_delete=models.CASCADE)
    groupID=models.ForeignKey("group",on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.articleID + ' and ' + self.groupID

class message(models.Model):
    group = models.ForeignKey(
        'group',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'personal.UserProfile',
        on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add= True)
