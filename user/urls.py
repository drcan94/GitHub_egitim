from django.urls import path
from .views import register, user_login, user_logout, user_profile, user_settings,user_password_change,user_about

urlpatterns = [
    path('register/', view=register, name="register"),
    path('login/', view=user_login, name="login"),
    path('logout/', view=user_logout, name="logout"),
    path('settings/', view=user_settings, name="user-settings"),
    path('(<username>$', view=user_profile, name="user-profile"),
    path('password_change/', view=user_password_change, name="password_change"),
    path('(<username>$/about-me/', view=user_about, name="about_me"),
]
