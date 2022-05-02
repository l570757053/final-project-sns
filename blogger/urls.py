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
    path("createcomment/<str:id>", views.createcomment, name="createcomment"),
    path("clike/<str:id>", views.clike, name="clike"),
    path("mlike/<str:id>", views.mlike, name="mlike"),
    path("collect/<str:id>", views.collect, name="collect"),
    path("relay/<str:id>", views.relay, name="relay"),
    path("bloginf/<str:id>", views.bloginf, name="bloginf"),
    path("mlike1/<str:id>", views.mlike1, name="mlike1"),
    path("listlike", views.listlike, name="listlike"),
    path("listcollect", views.listcollect, name="listcollect"),
    path("listcomment", views.listcomment, name="listcomment"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
