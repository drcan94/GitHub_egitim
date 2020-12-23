from django.db import models
from unidecode import unidecode
from django.template.defaultfilters import slugify,safe
from uuid import uuid4
import os
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

def upload_to(instance,filename):
    uzanti = filename.split(".")[-1]
    new_name = "%s.%s"%(str(uuid4()),uzanti)
    unique_id = instance.unique_id
    return os.path.join("resim",unique_id,new_name)

class Category(models.Model):
    isim = models.CharField(max_length = 10,verbose_name="Kategori İsim")
    class Meta:
        verbose_name_plural = "Kategoriler"
    def __str__(self):
        return self.isim

class Article(models.Model):

    YAYIN_TASLAK = ((None,"Yayın Türü Seçiniz"),("yayin","YAYIN"),("taslak","TASLAK"))

    user = models.ForeignKey(User,default=1,null=True,verbose_name="Kullanıcı",on_delete=models.CASCADE,related_name="article")

    title = models.CharField(max_length = 50,blank = False,null=True,verbose_name="Başlık")

    content = RichTextField(max_length=10000,blank=False,null=True,verbose_name="İçerik")

    slug = models.SlugField(null=True,unique=True,editable=False)

    image = models.ImageField(upload_to=upload_to,default='default/61733.png',verbose_name='Resim',null=True,blank=True)

    yayin_taslak = models.CharField(choices=YAYIN_TASLAK,max_length=6,null=True,blank=False)

    unique_id = models.CharField(max_length=100,editable=False,null=True)

    kategoriler = models.ManyToManyField(to=Category,related_name="article",null=True,blank=False)

    created_date = models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name="Oluşturulma Tarihi")   #auto_now güncelleme tarihi için

    class Meta:
        verbose_name_plural = "Spotlar"
        ordering = ['-created_date']

    def __str__(self):
        return "%s / %s"%(self.title,self.user)

    def get_added_favorite_user(self):
        return self.favorite_article.values_list('user__username',flat=True)

    def get_comment_count(self):
        yorum_sayisi = self.comments.count()
        if yorum_sayisi >0:
            return yorum_sayisi
        return "Henüz Yorum Yok"

    def get_favorite_count(self):
        favori_sayisi = self.favorite_article.count()
        if favori_sayisi > 0:
            return favori_sayisi
        return "Favorilere Eklenmedi"

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/default/61733.png'

    def get_unique_slug(self):
        sayi = 0
        slug = slugify(unidecode(self.title))
        new_slug=slug
        while Article.objects.filter(slug=new_slug).exists():
            sayi+=1
            new_slug= "%s-%s"%(slug,sayi)
        slug = new_slug
        return slug

    @classmethod
    def get_yayin_or_taslak(cls,yayin_taslak):
        return cls.objects.filter(yayin_taslak=yayin_taslak)


    def get_yayin_taslak_html(self):
        if self.yayin_taslak == "taslak":
            return safe("<span class='btn btn-{1}'>{0}</span>".format(self.get_yayin_taslak_display(),"danger"))
        return safe("<span class='btn btn-{1}'>{0}</span>".format(self.get_yayin_taslak_display(),"primary"))

    def save(self, *args,**kwargs):
        if self.id is None:
            new_unique_id = str(uuid4())
            self.unique_id = new_unique_id
            self.slug = self.get_unique_slug()
        else:
            article = Article.objects.get(slug=self.slug)
            if article.title != self.title:
                self.slug = self.get_unique_slug()
        super(Article, self).save(*args,**kwargs)

    def get_article_comment(self):
        return self.comments.all()

class Comment(models.Model):
    user = models.ForeignKey(User,null=True,default=1,related_name="comments",on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=True,on_delete=models.CASCADE, verbose_name="Spot", related_name="comments")
    comment_content = models.TextField(verbose_name="YORUM",max_length=1000,blank=False,null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Yorum Tarihi")

    class Meta:
        verbose_name_plural = "Yorumlar"
        ordering = ['-comment_date']

    def __str__(self):
        return "%s / %s"%(self.user,self.article)

    def get_screen_name(self):
        if self.user.first_name:
            return "%s" % (self.user.get_full_name())
        return self.user.username



class FavoriteArticle(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name="favorite_article", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE, verbose_name="Favori İçerik",
                                related_name="favorite_article")

    class Meta:
        verbose_name_plural="Favori İçerikler"

    def __str__(self):
        return "%s / %s" % (self.user,self.article)
