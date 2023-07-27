from django.urls import path, re_path, include

from . import views

urlpatterns = [
    re_path(r"^user/(?P<username>[\w@._-]*)$",
            views.view_user, name="get_user"),
    re_path(r"^user/(?P<username>[\w@._-]*)/$",
            views.view_user, name="get_user"),
    re_path(
        r"^user/(?P<username>[\w@.]*)/media$",
        views.view_user_media,
        name="get_user_media",
    ),
    re_path(
        r"^user/(?P<username>[\w@.]*)/playlists$",
        views.view_user_playlists,
        name="get_user_playlists",
    ),
    re_path(
        r"^user/(?P<username>[\w@.]*)/about$",
        views.view_user_about,
        name="get_user_about",
    ),
    re_path(r"^user/(?P<username>[\w@.]*)/edit$",
            views.edit_user, name="edit_user"),
    re_path(r"^channel/(?P<friendly_token>[\w]*)$",
            views.view_channel, name="view_channel"),
    re_path(
        r"^channel/(?P<friendly_token>[\w]*)/edit$",
        views.edit_channel,
        name="edit_channel",
    ),
]
