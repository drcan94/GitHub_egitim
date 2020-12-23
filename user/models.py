from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

# Create your models here.

class UserProfile(models.Model):
    about = models.TextField(max_length=2000, blank=True, null=True, verbose_name="Hakkımda")
    GENDER = ((None,'Tercihiniz'),('diger','DİĞER'),('erkek','ERKEK'),('kadın','KADIN'))
    gender = models.CharField(choices=GENDER,blank=True,null=True,max_length=10,verbose_name='Cinsiyet')
    profile_photo = models.ImageField(null=True,blank=True,verbose_name='Profil Fotoğrafı')
    dogum_tarihi = models.DateField(null=True,blank=True,verbose_name='Doğum Tarihi')
    user = models.OneToOneField(User,null=True,blank=False,verbose_name='User',on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Kullanıcı Profilleri"

    def get_usernames(self):
        user = get_user_model()
        users = user.objects.all()
        return users
    
    def get_screen_name(self):
        user=self.user
        if user.get_full_name():
            return user.get_full_name()
        return user.username

    def get_user_profile_url(self):
        url = reverse('user-profile',kwargs={'username':self.user.username})
        return url

    def user_full_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return None

    def get_profile_photo(self):
        if self.profile_photo:
            return self.profile_photo.url
        return "/static/img/default.jpg"

    def __str__(self):
        return "%s Profili"%(self.get_screen_name())

def create_profile(sender,created,instance,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)



post_save.connect(create_profile,sender=User)

