from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import RegisterForm, LoginForm, UserProfileUpdateForm, UserPasswordChange
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from article.decorators import anonymous_required
from .models import UserProfile, User
from article.models import Article
from following.models import Following


# Create your views here.
@anonymous_required
def register(request):
    form = RegisterForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, '<b>Kaydınız Gerçekleşti</b>', extra_tags='success')
                return HttpResponseRedirect(user.userprofile.get_user_profile_url())
    return render(request, 'user/register.html', context={'form': form})


@anonymous_required
def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                msg = "Merhaba <b>%s</b>, Tekrar Hoşgeldin" % (request.user.first_name)
                messages.success(request, msg, extra_tags='success')
                return HttpResponseRedirect(reverse('index'))
    return render(request, 'user/login.html', context={'form': form})


def user_logout(request):
    try:
        firstname = request.user.first_name
        logout(request)
        msg = "Tekrar Görüşmek Üzere <b>%s</b>" % (firstname)
        messages.success(request, msg, extra_tags='success')

        return HttpResponseRedirect(reverse('index'))
    except:
        msg = "Önce Giriş Yapmanız Gerekiyor"
        messages.success(request, msg, extra_tags='success')
        return HttpResponseRedirect(reverse('login'))


def user_profile(request, username):
    takip_kontrol = False
    user = User.objects.filter(username=username).first()
    articles = Article.objects.filter(user=user)
    follower_followed = Following.kullanici_follower_followed_count(user)
    followers = follower_followed["followers"]
    followeds = follower_followed["followeds"]
    if user != request.user:
        takip_kontrol = Following.takip_kontrol(follower=request.user, followed=user)

    return render(request, "user/profile/userprofile.html",
                  context={"followers": followers, "followeds": followeds, 'takip_kontrol': takip_kontrol, 'user': user,
                           'articles': articles, 'page': 'user-profile'})


def user_settings(request):
    gender = request.user.userprofile.gender
    about = request.user.userprofile.about
    profile_photo = request.user.userprofile.profile_photo
    dogum_tarihi = request.user.userprofile.dogum_tarihi
    follower_followed = Following.kullanici_follower_followed_count(request.user)
    followers = follower_followed["followers"]
    followeds = follower_followed["followeds"]
    initial = {"gender": gender, "about": about, "profile_photo": profile_photo, "dogum_tarihi": dogum_tarihi}
    form = UserProfileUpdateForm(initial=initial, instance=request.user, data=request.POST or None,
                                 files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=True)
            about = form.cleaned_data.get('about', None)
            gender = form.cleaned_data.get('gender', None)
            profile_photo = form.cleaned_data.get('profile_photo', None)
            dogum_tarihi = form.cleaned_data.get("dogum_tarihi", None)
            user.userprofile.gender = gender
            user.userprofile.about = about
            user.userprofile.dogum_tarihi = dogum_tarihi
            user.userprofile.profile_photo = profile_photo
            user.userprofile.save()
            messages.success(request, "Profil Bilgileriniz Güncellendi", extra_tags="success")
            return HttpResponseRedirect(reverse("user-settings"))
        else:
            messages.warning(request, "Lütfen Verileri Doğru Giriniz", extra_tags="danger")

    return render(request, "user/profile/settings.html", context={"followers": followers, "followeds": followeds,'form': form, 'page': 'settings'})


def user_password_change(request):
    form = UserPasswordChange(user=request.user, data=request.POST or None)
    follower_followed = Following.kullanici_follower_followed_count(request.user)
    followers = follower_followed["followers"]
    followeds = follower_followed["followeds"]
    if form.is_valid():
        new_password = form.cleaned_data.get("new_password")
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Şifreniz Değiştirildi", extra_tags="success")
        return HttpResponseRedirect(reverse("user-profile", kwargs={"username": request.user.username}))
    return render(request, "user/profile/password_change.html",
                  context={"followers": followers, "followeds": followeds, 'form': form, 'page': 'password_change'})


def user_about(request, username):
    takip_kontrol = False
    user = User.objects.filter(username=username).first()
    if user != request.user:
        takip_kontrol = Following.takip_kontrol(follower=request.user, followed=user)
    follower_followed = Following.kullanici_follower_followed_count(user)
    followers = follower_followed["followers"]
    followeds = follower_followed["followeds"]
    return render(request, "user/profile/about_me.html",
                  context={"followers": followers, "followeds": followeds, 'takip_kontrol': takip_kontrol, "user": user,
                           'page': 'about'})
