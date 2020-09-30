from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    #userIndex=models.IntegerField( null = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    name=models.CharField(max_length=20, null = False)
    intro=models.TextField(blank=True)
    def __str__(self):
    # return self.user.__str__()
    #return "{}".format(self.user.__str__())
        return self.name
class Meta:
    verbose_name = 'User profile'

