from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Following
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def kullanici_modal_following(request):
    response = sub_kullanici_takip_et_cikar(request)
    follow_type = request.GET.get("follow_type")
    owner = request.GET.get("owner")
    data = response.get("data")
    # followed = response.get("followed")

    myfolloweds = Following.get_followeds_username(user=request.user)
    if owner == request.user.username:
        kullanici_follower_followed_count = Following.kullanici_follower_followed_count(request.user)
        context = {"user": request.user, "followers": kullanici_follower_followed_count["followers"],
                   "followeds": kullanici_follower_followed_count["followeds"]}
        html_render_takip_durum = render_to_string("user/profile/include/following/following_part.html",
                                                   context=context, request=request)
        if follow_type == "followeds":
            following = Following.get_followeds(user=request.user)
            following = following_paginate(following,1)
            html = render_to_string("following/profile/include/followeds_followers_list.html",
                                    context={"following": following, "myfolloweds": myfolloweds,
                                             "follow_type": follow_type}, request=request)
            html_paginate = render_to_string("following/profile/include/show_more_button.html",
                                             context={"username": request.user.username, "following": following,
                                                      "follow_type": follow_type})
            data.update({"html": html,"html_paginate":html_paginate})

        data.update(
            {"follow_type": follow_type, "html_takip_render": html_render_takip_durum, "owner": True})
    else:
        data.update({"owner": False})

    return JsonResponse(data=data)


def kullanici_takip_et_cikar(request):
    response = sub_kullanici_takip_et_cikar(request)
    data = response.get("data")
    followed = response.get("followed")
    kullanici_follower_followed_count = Following.kullanici_follower_followed_count(followed)
    context = {"user": followed, "followers": kullanici_follower_followed_count["followers"],
               "followeds": kullanici_follower_followed_count["followeds"]}
    html = render_to_string("user/profile/include/following/following_part.html", context=context, request=request)
    data.update({"html": html})
    return JsonResponse(data=data)


def sub_kullanici_takip_et_cikar(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    data = {"takip_durum": True, "html": "", "is_valid": True, "msg": "<b>Takipten Çıkar</b>"}
    follower_username = request.GET.get("follower_username", None)
    followed_username = request.GET.get("followed_username", None)
    follower = get_object_or_404(User, username=follower_username)
    followed = get_object_or_404(User, username=followed_username)
    takip_kontrol = Following.takip_kontrol(follower=follower, followed=followed)
    if not takip_kontrol:
        Following.kullanici_takip_et(follower=follower, followed=followed)
    else:
        Following.kullanici_takipten_cikar(followed=followed, follower=follower)
        data.update({"msg": "<b>Takip Et</b>", "takip_durum": False})

    return {"data": data, "followed": followed}


def followeds_or_followers_list(request, follow_type):
    data = {"is_valid": True, "html": ""}
    page = request.GET.get("page", 1)
    username = request.GET.get("username", None)
    if not username:
        raise Http404
    user = get_object_or_404(User, username=username)
    myfolloweds = Following.get_followeds_username(user=request.user)
    if follow_type == "followeds":
        followeds = Following.get_followeds(user=user)
        followeds = following_paginate(queryset=followeds, page=page)
        html = render_to_string("following/profile/include/followeds_followers_list.html",
                                context={"following": followeds, "myfolloweds": myfolloweds,
                                         "follow_type": follow_type}, request=request)
        html_paginate = render_to_string("following/profile/include/show_more_button.html",
                                         context={"username": user.username, "following": followeds,
                                                  "follow_type": follow_type})

    elif follow_type == "followers":
        followers = Following.get_followers(user=user)
        followers = following_paginate(queryset=followers, page=page)
        html = render_to_string("following/profile/include/followeds_followers_list.html",
                                context={"following": followers, "myfolloweds": myfolloweds,
                                         "follow_type": follow_type}, request=request)
        html_paginate = render_to_string("following/profile/include/show_more_button.html",
                                         context={"username": user.username, "following": followers,
                                                  "follow_type": follow_type})

    else:
        raise Http404
    data.update({"html": html, "html_paginate": html_paginate})
    return JsonResponse(data=data)


def following_paginate(queryset, page):
    paginator = Paginator(queryset, 10)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return queryset
