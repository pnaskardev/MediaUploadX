from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r"^$", views.index),
    re_path(r"^about", views.about, name="about"),
    # re_path(r"^add_subtitle", views.add_subtitle, name="add_subtitle"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
