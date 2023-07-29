from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path, re_path


from . feeds import IndexRSSFeed, SearchRSSFeed
from . import views

urlpatterns = [
    re_path(r"^$", views.index),
    re_path(r"^about", views.about, name="about"),
    re_path(r"^add_subtitle", views.add_subtitle, name="add_subtitle"),
    re_path(r"^categories$", views.categories, name="categories"),
    re_path(r"^contact$", views.contact, name="contact"),
    re_path(r"^edit", views.edit_media, name="edit_media"),
    re_path(r"^embed", views.embed_media, name="get_embed"),
    re_path(r"^featured$", views.featured_media),
    re_path(r"^fu/", include(("uploader.urls", "uploader"), namespace="uploader")),
    re_path(r"^history$", views.history, name="history"),
    re_path(r"^liked$", views.liked_media, name="liked_media"),
    re_path(r"^latest$", views.latest_media),
    re_path(r"^members", views.members, name="members"),
    re_path(
        r"^playlist/(?P<friendly_token>[\w]*)$",
        views.view_playlist,
        name="get_playlist",
    ),
    re_path(
        r"^playlists/(?P<friendly_token>[\w]*)$",
        views.view_playlist,
        name="get_playlist",
    ),
    re_path(r"^popular$", views.recommended_media),
    re_path(r"^recommended$", views.recommended_media),
    path("rss/", IndexRSSFeed()),
    re_path("^rss/search", SearchRSSFeed()),
    re_path(r"^search", views.search, name="search"),
    re_path(r"^scpublisher", views.upload_media, name="upload_media"),
    re_path(r"^tags", views.tags, name="tags"),
    re_path(r"^tos$", views.tos, name="terms_of_service"),
    re_path(r"^view", views.view_media, name="get_media"),
    re_path(r"^upload", views.upload_media, name="upload_media"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
