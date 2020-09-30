from django.contrib import admin
from article import models
# Register your models here.

# admin.site.register(models.article)
admin.site.register(models.tag)
admin.site.register(models.category)
admin.site.register(models.comment)
# admin.site.register(models.Post)
class articleAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.article, articleAdmin)