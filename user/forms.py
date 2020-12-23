from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re
from .models import UserProfile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='Şifre')

    confirm = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                              label='Şifreyi Doğrula')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs = {"class": "form-control"}
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        if password != confirm:
            self.add_error('confirm', 'Şifreler Eşleşmiyor')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-mail sistemde kayıtlı")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı sistemde kayıtlı")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, label='Kullanıcı Adı',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, max_length=50, label='Şifre',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Hatalı Kullanıcı Adı veya Şifre')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            users = User.objects.filter(email__iexact=username)
            if len(users) > 0 and len(users) == 1:
                return users.first().username
        return username


class UserProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(required=False, choices=UserProfile.GENDER)
    profile_photo = forms.ImageField(required=False)
    about = forms.CharField(widget=forms.Textarea,required=False)
    dogum_tarihi = forms.DateField(input_formats=("%d.%m.%Y",),widget=forms.DateInput(format="%d.%m.%Y"),required=True, label='Doğum Tarihi')
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "gender","dogum_tarihi","profile_photo","about"]

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs = {"class": "form-control"}
        self.fields["about"].widget.attrs["rows"] = 10

    def clean_email(self):
        email = self.cleaned_data.get('email',None)
        if not email:
            raise forms.ValidationError("Lütfen E-Mail Adresinizi Giriniz")

        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError("Bu e-mail sistemde kayıtlı")
        return email

class UserPasswordChange(forms.Form):
    old_password = forms.CharField(required=True,min_length=5,label="Mevcut Şifreniz",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(required=True,min_length=5,label="Yeni Şifreniz",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password_confirm = forms.CharField(required=True,min_length=5,label="Yeni Şifrenizi Doğrulayın",widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserPasswordChange, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        new_password_confirm = self.cleaned_data.get("new_password_confirm")
        if new_password != new_password_confirm:
            self.add_error("new_password_confirm","Yeni Şifreler Uyuşmuyor")

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Lütfen Mevcut Şifrenizi Giriniz")
        return old_password

