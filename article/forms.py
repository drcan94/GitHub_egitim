from django import forms
from .models import Article,Comment
from ckeditor.widgets import CKEditorWidget


banned_emails=["abc@gmail.com","xyz@gmail.com"]

class IletisimForm(forms.Form):
    isim = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}), max_length=50,label="İsim",required=False)
    soyisim = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),max_length=50,label="Soyisim",required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}),max_length=50,label="E-Mail",required=True)
    email2 = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}),max_length=50,label="E-Mail Kontrol",required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), max_length=50, label="İçerik", required=True)

    def __init__(self,*args,**kwargs):
        super(IletisimForm, self).__init__(*args,**kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs={"class":"form-control"}

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email == "drcan94@gmail.com":
            raise forms.ValidationError("Bunu Kullanamazsın ;)")
        elif email in banned_emails:
            raise forms.ValidationError("Bu Adres Banlandı ;)")
        return email
    def clean(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email != email2:
            self.add_error("email2","E-Mail'ler Uyuşmuyor")
            #raise forms.ValidationError("E-Mail'ler Uyuşmuyor")


class BlogForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","content","image","yayin_taslak","kategoriler"]

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs = {"class": "form-control"}
        self.fields["content"].widget.attrs["rows"]=10
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 20:
            msg="Lütfen en az 20 karakter giriniz, şuanki karakter sayısı (%s)"%(len(content))
            raise forms.ValidationError(msg)
        return content

class SpotSorguForm(forms.Form):
    YAYIN_TASLAK = (("all", "HEPSİ"), ("yayin", "YAYIN"), ("taslak", "TASLAK"))
    search = forms.CharField(required=False,max_length=500,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Aramak İstediğiniz Kelime?"}))
    yayin_taslak = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}),choices=YAYIN_TASLAK,required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_content"]
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs = {"class":"form-control"}















