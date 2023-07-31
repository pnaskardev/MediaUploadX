from django.urls import path, re_path, include
from . import api
from .feeds import IndexRSSFeed, SearchRSSFeed
from . import views, management_views

urlpatterns = [
    # Regular path patterns
    path("", views.index),
    path("about/", views.about, name="about"),
    path("add_subtitle/", views.add_subtitle, name="add_subtitle"),
    path("categories/", views.categories, name="categories"),
    path("contact/", views.contact, name="contact"),
    path("edit/", views.edit_media, name="edit_media"),
    path("embed/", views.embed_media, name="get_embed"),
    path("featured/", views.featured_media),
    
    # Include another URL patterns file (uploader.urls)
    re_path(r"^fu/", include(("uploader.urls", "uploader"), namespace="uploader")),
    
    path("history/", views.history, name="history"),
    path("liked/", views.liked_media, name="liked_media"),
    path("latest/", views.latest_media),
    path("members/", views.members, name="members"),
    
    # URL patterns with named parameters
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
    
    path("popular/", views.recommended_media),
    path("recommended/", views.recommended_media),
    
    # RSS feed patterns
    path("rss/", IndexRSSFeed()),
    re_path("^rss/search", SearchRSSFeed()),
    
    path("search/", views.search, name="search"),
    path("scpublisher/", views.upload_media, name="upload_media"),
    path("tags/", views.tags, name="tags"),
    path("tos/", views.tos, name="terms_of_service"),
    path("view/", views.view_media, name="get_media"),
    path("upload/", views.upload_media, name="upload_media"),
    
    # API URL patterns
    re_path(r"^api/v1/media$", api.MediaList.as_view()),
    re_path(
        r"^api/v1/media/(?P<friendly_token>[\w]*)$",
        api.MediaDetail.as_view(),
        name="api_get_media",
    ),
    re_path(
        r"^api/v1/media/encoding/(?P<encoding_id>[\w]*)$",
        api.EncodingDetail.as_view(),
        name="api_get_encoding",
    ),
    re_path(r"^api/v1/search$", api.MediaSearch.as_view()),
    
    # More API URL patterns...
    
    re_path(
        r"^api/v1/media/(?P<friendly_token>[\w]*)/actions$",
        api.MediaActions.as_view(),
    ),
    re_path(r"^api/v1/categories$", api.CategoryList.as_view()),
    re_path(r"^api/v1/tags$", api.TagList.as_view()),
    re_path(r"^api/v1/comments$", api.CommentList.as_view()),
    re_path(
        r"^api/v1/media/(?P<friendly_token>[\w]*)/comments$",
        api.CommentDetail.as_view(),
    ),
    re_path(
        r"^api/v1/media/(?P<friendly_token>[\w]*)/comments/(?P<uid>[\w-]*)$",
        api.CommentDetail.as_view(),
    ),
    re_path(r"^api/v1/playlists$", api.PlaylistList.as_view()),
    re_path(r"^api/v1/playlists/$", api.PlaylistList.as_view()),
    re_path(
        r"^api/v1/playlists/(?P<friendly_token>[\w]*)$",
        api.PlaylistDetail.as_view(),
        name="api_get_playlist",
    ),
    re_path(r"^api/v1/user/action/(?P<action>[\w]*)$", api.UserActions.as_view()),


    # ADMIN VIEWS URL patterns
    re_path(r"^api/v1/encode_profiles/$", api.EncodeProfileList.as_view()),
    re_path(r"^api/v1/manage_media$", management_views.MediaList.as_view()),
    re_path(r"^api/v1/manage_comments$", management_views.CommentList.as_view()),
    re_path(r"^api/v1/manage_users$", management_views.UserList.as_view()),
    re_path(r"^api/v1/tasks$", api.TasksList.as_view()),
    re_path(r"^api/v1/tasks/(?P<friendly_token>[\w|\W]*)$", api.TaskDetail.as_view()),
    
    path("manage/comments/", views.manage_comments, name="manage_comments"),
    path("manage/media/", views.manage_media, name="manage_media"),
    path("manage/users/", views.manage_users, name="manage_users"),
]
