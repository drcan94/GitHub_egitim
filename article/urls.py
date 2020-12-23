from django.urls import path
from article import views

urlpatterns = [
    path('create/', views.createArticle, name="create"),
    path('detail/(<slug>$', views.detailArticle, name="detail"),
    path('update/(<slug>$', views.updateArticle, name="update"),
    path('delete/(<slug>$', views.deleteArticle, name="delete"),
    path('spots/', views.spotsArticle, name="spots"),
    path('add-comment/(<slug>$', views.add_comment, name="add-comment"),
    path('favorite-page/(<slug>$/', views.add_or_remove_favorite, name="favorite-page"),

]
