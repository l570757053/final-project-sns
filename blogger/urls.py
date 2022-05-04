from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("publish", views.publish, name="publish"),
    path("user/<str:u_id>", views.showuser),
    path("createcomment/<str:m_id>", views.createcomment, name="createcomment"),
    path("clike/<str:m_id>", views.clike, name="clike"),
    path("mlike/<str:m_id>", views.mlike, name="mlike"),
    path("collect/<str:m_id>", views.collect, name="collect"),
    path("relay/<str:m_id>", views.relay, name="relay"),
    path("bloginf/<str:m_id>", views.bloginf, name="bloginf"),
    path("mlike1/<str:m_id>", views.mlike1, name="mlike1"),
    path("listlike", views.listlike, name="listlike"),
    path("listcollect", views.listcollect, name="listcollect"),
    path("listcomment", views.listcomment, name="listcomment"),
    path("listfollow", views.listfollow, name="listfollow"),
    path("listfan", views.listfan, name="listfan"),
    path("cu", views.cu, name="cu"),
    path("changeuser", views.changeuser, name="changeuser"),
    path("notice", views.notice, name="notice"),
    path("search", views.search, name="search"),
    path("changecolor/", views.color, name="color"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
