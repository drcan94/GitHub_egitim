from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse
from .models import Article,User,FavoriteArticle
from django.http import HttpResponseBadRequest,HttpResponseForbidden,JsonResponse
from .forms import IletisimForm,BlogForm,SpotSorguForm,CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .decorators import is_post
from django.template.loader import render_to_string

# Create your views here.


def index(request):
    return render(request,"tblog/index.html")

def about(request):
    return render(request,"about.html")


def spotsArticle(request):
    #x = "Naber Dünya"
    #y = "İyidir Senden"
    #z = [25,"04",1994]
    #return render(request,"tblog/spots.html",context={"i":x,"j":y,"h":z})        # x değişkenini i olarak template e aktardık

    #spots = Article.objects.all()
    #sayi=10
    #context={"spots":spots,"sayi":sayi}
    #return render(request,"tblog/spots.html",context)
    spots = Article.objects.all()
    page = request.GET.get("page",1)
    form = SpotSorguForm(data=request.GET or None)
    if form.is_valid():
        yayin_taslak = form.cleaned_data.get("yayin_taslak")
        search = form.cleaned_data.get("search",None)
        if search:
            spots=spots.filter(Q(content__icontains=search)|Q(title__icontains=search)|Q(kategoriler__isim__icontains=search))
        if yayin_taslak and yayin_taslak != "all":
            spots=spots.filter(yayin_taslak=yayin_taslak)

    paginator = Paginator(spots,4)
    try:
        spots = paginator.page(page)
    except EmptyPage:
        spots = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        spots = paginator.page(1)

    context={"spots":spots,"form":form}
    return render(request,"tblog/spots.html",context)

@login_required
def updateArticle(request,slug):
    article = Article.objects.filter(slug=slug).first()
    if request.user != article.user:
        return HttpResponseForbidden()
    form = BlogForm(instance=article,data=request.POST or None,files=request.FILES or None)
    if form.is_valid():
        article = form.save()
        print(article.kategoriler)
        msg = "%s başlıklı spot güncellendi!" % (article.title)
        messages.success(request, msg,extra_tags="success")
        url = reverse("detail", kwargs={"slug": article.slug})
        return HttpResponseRedirect(url)
    return render(request,"tblog/update.html",context={"form":form})

@login_required
def deleteArticle(request,slug):
    article = Article.objects.filter(slug=slug).first()
    if request.user != article.user:
        return HttpResponseForbidden()
    article.delete()
    msg = "%s başlıklı spot silindi!" % (article.title)
    messages.success(request, msg,extra_tags="danger")
    url = reverse("spots")
    return HttpResponseRedirect(url)

@login_required
def createArticle(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article = form.save()
            print(article.kategoriler)
            msg = "Tebrikler %s başlıklı spotu başarıyla oluşturdunuz!" %(article.title)
            messages.success(request,msg,extra_tags="success")
            url = reverse("detail",kwargs={"slug":article.slug})
            return HttpResponseRedirect(url)
    return render(request,"tblog/create.html",context={"form":form})

@login_required
def detailArticle(request,slug):
    form = CommentForm()
    article = Article.objects.filter(slug=slug).first()
    comments = article.comments.all()
    return render(request,"tblog/detail.html",context={"article":article,"form":form,"comments":comments})

@login_required
@is_post
def add_comment(request,slug):
    article = Article.objects.filter(slug=slug).first()
    form = CommentForm(data=request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.article = article
        new_comment.user = request.user
        new_comment.save()
        messages.success(request,"Yorumunuz Eklendi")
    return HttpResponseRedirect(reverse("detail", kwargs={"slug": article.slug}))


@login_required
def add_or_remove_favorite(request,slug):
    url = request.GET.get('next',None)
    article = Article.objects.filter(slug=slug).first()
    favorite_article = FavoriteArticle.objects.filter(article=article,user=request.user)
    if favorite_article.exists():
        favorite_article.delete()
    else:
        FavoriteArticle.objects.create(article=article,user=request.user)
    return HttpResponseRedirect(url)

mesajlar = []
def iletisim(request):
    form = IletisimForm(data=request.GET or None)
    if form.is_valid():
        isim = form.cleaned_data.get("isim")
        soyisim = form.cleaned_data.get("soyisim")
        email = form.cleaned_data.get("email")
        content = form.cleaned_data.get("content")
        data = {"isim":isim,"soyisim":soyisim,"email":email,"content":content}
        mesajlar.append(data)
        return render(request,"iletisim.html",context={"mesajlar":mesajlar,"form":form})
    return render(request,"iletisim.html",context={"form":form})




def biz(request):
    return render(request,"tblog/sadecebizeait.html")


def deneme(request):
    if request.is_ajax():
        context = {"msg":"Candır","is_valid":True}
        return JsonResponse(data=context)
    return render(request,"deneme.html")

def deneme_ajax(request):
    if not request.is_ajax():
         return HttpResponseBadRequest()
    isim = request.POST.get("isim")
    return JsonResponse(data={"isim":isim,"msg":"drcan94"})

def deneme_ajax2(request):
    if not request.is_ajax():
         return HttpResponseBadRequest()
    context = {"ogrenci":{"isim_soyisim":"Burak Can","ogretmen_isim_soyisim":"Ali Akbulut"}}
    html = render_to_string("veliyemesaj.html",context=context,request=request)
    data = {"html":html}
    return JsonResponse(data=data)