from django.db import models
from personal.models import UserProfile
from simditor.fields import RichTextField
# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100,default="未分類")
    creater=models.ForeignKey("personal.UserProfile",on_delete=models.CASCADE,null=True)
    class Meta:
        unique_together = ('name', 'creater',)
    def __str__(self):
        return 'category:'+ self.name+' creater: '+self.creater.name
class tag(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return 'tag:'+ self.name
class article(models.Model):
    title=models.CharField(max_length=20,null=False)
    private=models.IntegerField(default=0) #文章隱私設定: 0:公開 1:私有 2:只有群組成員可以看
    # content=RichTextField() #這個後臺也彙編成編輯器的樣子
    content=models.TextField()
    author=models.ForeignKey("personal.UserProfile",on_delete=models.CASCADE) #cascade指刪除時，相關聯的都刪掉
    pubtime=models.DateTimeField(auto_now_add= True)
    like=models.FloatField(default=0)
    tags = models.ManyToManyField(tag, blank=True)
    categorys = models.ManyToManyField(category)
    
    def __str__(self):
        return 'Article:'+ self.title+' like: '+str(self.like)



class comment(models.Model):
    post=models.ForeignKey("article",on_delete=models.DO_NOTHING)
    created_by=models.ForeignKey("personal.UserProfile",on_delete=models.DO_NOTHING,null=True)
    parent_id=models.IntegerField(default=0)
    content=models.TextField(null= False)
    created_at=models.DateTimeField(auto_now= True)
    def __str__(self):
        return 'comment:'+ self.content