from django.db import models
from django.contrib.auth.models import User


class Following(models.Model):
    follower = models.ForeignKey(User, null=True, related_name="follower", verbose_name='Takipçi',
                                 on_delete=models.CASCADE)
    followed = models.ForeignKey(User, null=True, related_name="followed", verbose_name='Takip Edilen',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Takipleşme Sistemi"

    def __str__(self):
        return "Takipçi : {} / Takip Edilen : {}".format(self.follower.username, self.followed.username)

    @classmethod
    def kullanici_takip_et(cls, follower, followed):
        cls.objects.create(follower=follower, followed=followed)

    @classmethod
    def kullanici_takipten_cikar(cls, follower, followed):
        cls.objects.filter(follower=follower, followed=followed).delete()

    @classmethod
    def takip_kontrol(cls, follower, followed):
        return cls.objects.filter(follower=follower, followed=followed).exists()

    @classmethod
    def kullanici_follower_followed_count(cls, user):
        data = {"followeds": 0, "followers": 0}
        followeds = cls.objects.filter(follower=user).count()
        followers = cls.objects.filter(followed=user).count()
        data.update({"followeds": followeds, "followers": followers})
        return data

    @classmethod
    def get_followers(cls,user):
        return cls.objects.filter(followed=user)

    @classmethod
    def get_followeds(cls,user):
        return cls.objects.filter(follower=user)

    @classmethod
    def get_followeds_username(cls,user):
        followeds = cls.get_followeds(user)
        return followeds.values_list("followed__username",flat=True)