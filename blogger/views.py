from email import message
from itertools import count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from . import models
from .models import Background, Follow, Notice, User,Message,Cikes,Mlikes,Comment,Collect


def index(request):
    if request.user.is_authenticated:
        f = models.Follow.objects.filter(fans=request.user).values_list('following', flat=True)
        
        #msgs = models.Message.objects.select_related('user').filter(Q(user__in=f) | Q(user=request.user))
        msgs = models.Message.objects.select_related('user').filter(show=True)
        a=Background.objects.get(user=request.user)

        return render(request, "index.html", {
            'msgs': msgs,
            "a":a
        })
    else:
        msgs = models.Message.objects.select_related('user').filter(show=True)
        return render(request, "index.html", {
            'msgs': msgs
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        picture = request.FILES.get("picture")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.profilePhoto = picture
            notice = models.Notice(user=user)
            background = models.Background(user=user)
            user.save()
            notice.save()
            background.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def publish(request):
    content = request.POST["content"]
    h = request.POST["h"]
    picture = request.FILES.get("picture")
    # 公开
    if h == "n":
        show = True
    # 粉丝可见
    else:
        show = False
    msg = models.Message(user=request.user, content=content, show=show, pic=picture)
    msg.save()
    return HttpResponseRedirect(reverse("index"))


def showuser(request, u_id):
    if request.method == "GET":
        user = models.User.objects.get(username=u_id)
        ctx = {'c_style': "col-sm-offset-3", 'user': user}
        if request.user == user:
            ctx['flag'] = False
            msgs = models.Message.objects.filter(user=u_id)
            ctx['msgs'] = msgs
        else:
            msgs = models.Message.objects.filter(user=u_id, show=True)
            ctx['msgs'] = msgs
            ctx['flag'] = True
            fol = models.Follow.objects.filter(following=user, fans=request.user)
            if fol:
                ctx['btn_class'] = "btn btn-success"
            else:
                ctx['btn_class'] = "btn btn-default"
        return render(request, "user.html", ctx)
    else:
        # TODO: 需要填充关注和修改签名，h的值为fol是关注，cha则是修改
        return HttpResponseRedirect("/user/"+u_id)


   
def clike(request,id):
    m=Comment.objects.get(ID=id)
    user=request.user
    if Cikes.objects.filter(comment_id=m,user=user):
        a=Cikes.objects.get(comment_id=m,user=user)
        a.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        c=Cikes.objects.create(comment_id=m,user=user)
        c.save()
        if Notice.objects.filter(user=m.user):
            notice=Notice.objects.get(user=m.user)
            notice.likes=notice.likes+1
            notice.save()
        else:
            notice=Notice.objects.create(user=m.user)
            notice.likes=notice.likes+1
            notice.save()
        return HttpResponseRedirect(reverse("index"))


def createcomment(request,id):
    m=Message.objects.get(ID=id)
    user=request.user
    comment=request.POST["content"]
    c=Comment.objects.create(message_id=m,user=user,content=comment)
    c.save()
    if Notice.objects.filter(user=m.user):
        notice=Notice.objects.get(user=m.user)
        notice.comments=notice.comment+1
        notice.save()
    else:
        notice=Notice.objects.create(user=m.user)
        notice.comments=notice.comment+1
        notice.save()
    return HttpResponseRedirect("/bloginf/"+id)


def mlike(request,id):
    m=Message.objects.get(ID=id)
    user=request.user
    if Mlikes.objects.filter(message_id=m,user=user):
        a=Mlikes.objects.get(message_id=m,user=user)
        a.delete()
        #a.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        c=Mlikes.objects.create(message_id=m,user=user)
        c.save()
        if Notice.objects.filter(user=m.user):
            notice=Notice.objects.get(user=m.user)
            notice.likes=notice.likes+1
            notice.save()
        else:
            notice=Notice.objects.create(user=m.user)
            notice.likes=notice.likes+1
            notice.save()
        return HttpResponseRedirect(reverse("index"))



def collect(request,id):
    m=Message.objects.get(ID=id)
    user=request.user
    if Collect.objects.filter(message_id=m,user=user):
        a=Collect.objects.get(message_id=m,user=user)
        a.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        c=Collect.objects.create(message_id=m,user=user)
        c.save()
        return HttpResponseRedirect(reverse("index"))

def relay(request,id):
    m=Message.objects.get(ID=id)
    content=request.POST["content"]
    content=content+"//@"+m.user.username+":"+m.content
    user=request.user
    r=Message.objects.create(user=user,content=content,o_ID=id)
    if Notice.objects.filter(user=m.user):
        notice=Notice.objects.get(user=m.user)
        notice.relays=notice.relays+1
        notice.save()
    else:
        notice=Notice.objects.create(user=m.user)
        notice.relays=notice.relays+1
        notice.save()
    r.save()
    return HttpResponseRedirect(reverse("index"))


def bloginf(request,id):
    f = models.Follow.objects.filter(fans=request.user).values_list('following', flat=True)
    msgs = models.Message.objects.select_related('user').get(ID=id)
    cms=models.Comment.objects.select_related('user').filter(message_id=id)
    return render(request,"bloginf.html",{"msg":msgs,"cms":cms})



def mlike1(request,id):
    m=Message.objects.get(ID=id)
    user=request.user
    if Mlikes.objects.filter(message_id=m,user=user):
        a=Mlikes.objects.get(message_id=m,user=user)
        a.delete()
        #a.save()
        return HttpResponseRedirect("/bloginf/"+id)
    else:
        c=Mlikes.objects.create(message_id=m,user=user)
        c.save()
        if Notice.objects.filter(user=m.user):
            notice=Notice.objects.get(user=m.user)
            notice.likes=notice.likes+1
            notice.save()
        else:
            notice=Notice.objects.create(user=m.user)
            notice.likes=notice.likes+1
            notice.save()
        return HttpResponseRedirect("/bloginf/"+id)


def listlike(request):
    user=request.user
    mlike=Mlikes.objects.filter(user=user).select_related('message_id')
    clike=Cikes.objects.filter(user=user).select_related('comment_id')
    return render(request,"listl.html",{"mlikes":mlike,"clikes":clike})

def listcollect(request):
    user=request.user
    collect=Collect.objects.filter(user=user)
    return render(request,"listl.html",{"mlikes":collect})

def listcomment(request):
    user=request.user
    comments=Comment.objects.filter(user=user).select_related('message_id')
    return render(request,"listl.html",{"coms":comments})

def changeinf(request):
    user=request.user
    inf=request.POST["change_inf"]
    user.introduction=inf
    user.save()
    return HttpResponseRedirect("/user/"+user.username)

def follow(request,id):
    f=User.objects.get(username=id)
    fan=request.user
    fa=Follow.objects.create(following=f,fans=fan)
    fa.save()
    if Notice.objects.filter(user=f):
        notice=Notice.objects.get(user=f)
        notice.fans=notice.fans+1
        notice.save()
    else:
        notice=Notice.objects.create(user=f)
        notice.fans=notice.fans+1
        notice.save()
    return HttpResponseRedirect("/user/"+f.username)

def listfollow(request):
    user=request.user
    f=Follow.objects.filter(fans=user)
    return render(request,"listfollow.html",{"fs":f,"content":"关注"})

def listfan(request):
    user=request.user
    f=Follow.objects.filter(following=user)
    return render(request,"listfollow.html",{"fs":f,"content":"粉丝"})

def changeuser(request):
    user=request.user
    email = request.POST["email"]
    pic = request.FILES.get("pic")
    user.email=email
    user.profilePhoto=pic
    user.save()
    return HttpResponseRedirect("cu")

def cu(request):
    user=request.user
    return render(request,"changeuser.html",{"user":user})

def notice(request):
    user=request.user
    n=Notice.objects.get(user=user)
    likes = n.likes
    relays = n.relays
    comments = n.comments
    fans=n.fans
    n.likes = 0
    n.relays =0
    n.comments = 0
    n.fans=0
    n.save()
    return render(request,"notice.html",{"likes":likes,"relays":relays,"comments":comments,"fans":fans})


def search(request):
    text=request.POST["text"]
    ms=Message.objects.all()
    m=[i for i in ms if text in i.content]
    us=User.objects.all()
    u=[i for i in us if text in i.username]
    return render(request,"result.html",{"ms":m,"us":u})

def back(request):
    user=request.user
    if Background.objects.filter(user=user):
        a=Background.objects.get(user=user)
    else:
        a=Background.objects.create(user=user)    
    return render(request,"changeback.html",{"a":a})

def color(request):
    c=request.POST['color']
    user=request.user
    a=Background.objects.get(user=user)
    a.Font_color=c
    a.save()
    return HttpResponseRedirect("back")