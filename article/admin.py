from django.contrib import admin
from .models import Article,Category,Comment,FavoriteArticle

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title","user","created_date","content"]
    list_display_links=["title","created_date"]      #basıldığında makaleye gitmesi için

    search_fields = ["title"]
    list_filter = ["title","created_date"]
    class Meta:
        model = Article


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(FavoriteArticle)
