from django.contrib import admin
from group import models
# Register your models here.
class groupAdmin(admin.ModelAdmin):
    list_display=('name','intro','owner','createTime')

class memberAdmin(admin.ModelAdmin):
    list_display=('groupID','memberID','state')

class article_GroupAdmin(admin.ModelAdmin):
    list_display=('id','groupID','articleID')

class groupCategoriesAdmin(admin.ModelAdmin):
    list_display=('id','name','group')
class articleGroup_category_Admin(admin.ModelAdmin):
    list_display=('id','categoryID','articleID')

class messageAdmin(admin.ModelAdmin):
    list_display=('message','group','owner')

admin.site.register(models.group,groupAdmin)
admin.site.register(models.member,memberAdmin)
admin.site.register(models.articleGroup,article_GroupAdmin)
admin.site.register(models.group_category,groupCategoriesAdmin)
admin.site.register(models.articleGroup_category,articleGroup_category_Admin)
admin.site.register(models.message,messageAdmin)