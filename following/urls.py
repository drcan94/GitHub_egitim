from django.urls import path
from following import views
urlpatterns = [
    path('following', views.kullanici_takip_et_cikar, name="following"),
    path('follow_list/(<follow_type>$/', views.followeds_or_followers_list, name="follow_list"),
    path('modal_following', views.kullanici_modal_following, name="modal_following"),
]