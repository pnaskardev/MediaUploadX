from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from . models import (
    Category,
    Comment,
    EncodeProfile,
    Encoding,
    Media,
    Playlist,
    PlaylistMedia,
    Tag,
)
from .tasks import save_user_action
from . forms import SubtitleForm, ContactForm, MediaForm
from core.permissions import IsAuthorizedToAdd, IsUserOrEditor, user_allowed_to_upload
from .helpers import clean_query, get_alphanumeric_only, produce_ffmpeg_commands
from .methods import (
    check_comment_for_mention,
    get_user_or_session,
    is_mediauploadx_editor,
    is_mediauploadx_manager,
    list_tasks,
    notify_user_on_comment,
    show_recommended_media,
    show_related_media,
    update_user_ratings,
)


def index(request):
    """Index view"""

    context = {}
    return render(request, "core/index.html", context)


def about(request):
    """About view"""

    context = {}
    return render(request, "core/about.html", context)


@login_required
def add_subtitle(request):
    """Add subtitle view"""

    friendly_token = request.GET.get("m", "").strip()
    if not friendly_token:
        return HttpResponseRedirect("/")
    media = Media.objects.filter(friendly_token=friendly_token).first()
    if not media:
        return HttpResponseRedirect("/")

    if not (request.user == media.user or is_mediauploadx_editor(request.user) or is_mediauploadx_manager(request.user)):
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = SubtitleForm(media, request.POST, request.FILES)
        if form.is_valid():
            subtitle = form.save()
            messages.add_message(request, messages.INFO, "Subtitle was added!")
            return HttpResponseRedirect(subtitle.media.get_absolute_url())
    else:
        form = SubtitleForm(media_item=media)
    return render(request, "core/add_subtitle.html", {"form": form})


def categories(request):
    """List categories view"""

    context = {}
    return render(request, "core/categories.html", context)


def contact(request):
    """Contact view"""

    context = {}
    if request.method == "GET":
        form = ContactForm(request.user)
        context["form"] = form

    else:
        form = ContactForm(request.user, request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                from_email = request.user.email
                name = request.user.name
            else:
                from_email = request.POST.get("from_email")
                name = request.POST.get("name")
            message = request.POST.get("message")

            title = "[{}] - Contact form message received".format(
                settings.PORTAL_NAME)

            msg = """
You have received a message through the contact form\n
Sender name: %s
Sender email: %s\n
\n %s
""" % (
                name,
                from_email,
                message,
            )
            email = EmailMessage(
                title,
                msg,
                settings.DEFAULT_FROM_EMAIL,
                settings.ADMIN_EMAIL_LIST,
                reply_to=[from_email],
            )
            email.send(fail_silently=True)
            success_msg = "Message was sent! Thanks for contacting"
            context["success_msg"] = success_msg

    return render(request, "core/contact.html", context)


def history(request):
    """Show personal history view"""

    context = {}
    return render(request, "core/history.html", context)


@login_required
def edit_media(request):
    """Edit a media view"""

    friendly_token = request.GET.get("m", "").strip()
    if not friendly_token:
        return HttpResponseRedirect("/")
    media = Media.objects.filter(friendly_token=friendly_token).first()

    if not media:
        return HttpResponseRedirect("/")

    if not (request.user == media.user or is_mediauploadx_editor(request.user) or is_mediauploadx_manager(request.user)):
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = MediaForm(request.user, request.POST,
                         request.FILES, instance=media)
        if form.is_valid():
            media = form.save()
            for tag in media.tags.all():
                media.tags.remove(tag)
            if form.cleaned_data.get("new_tags"):
                for tag in form.cleaned_data.get("new_tags").split(","):
                    tag = get_alphanumeric_only(tag)
                    tag = tag[:99]
                    if tag:
                        try:
                            tag = Tag.objects.get(title=tag)
                        except Tag.DoesNotExist:
                            tag = Tag.objects.create(
                                title=tag, user=request.user)
                        if tag not in media.tags.all():
                            media.tags.add(tag)
            messages.add_message(request, messages.INFO, "Media was edited!")
            return HttpResponseRedirect(media.get_absolute_url())
    else:
        form = MediaForm(request.user, instance=media)
    return render(
        request,
        "core/edit_media.html",
        {"form": form, "add_subtitle_url": media.add_subtitle_url},
    )


def embed_media(request):
    """Embed media view"""

    friendly_token = request.GET.get("m", "").strip()
    if not friendly_token:
        return HttpResponseRedirect("/")

    media = Media.objects.values("title").filter(
        friendly_token=friendly_token).first()

    if not media:
        return HttpResponseRedirect("/")

    context = {}
    context["media"] = friendly_token
    return render(request, "core/embed.html", context)


def featured_media(request):
    """List featured media view"""

    context = {}
    return render(request, "core/featured-media.html", context)


def index(request):
    """Index view"""

    context = {}
    return render(request, "core/index.html", context)


def latest_media(request):
    """List latest media view"""

    context = {}
    return render(request, "core/latest-media.html", context)


def liked_media(request):
    """List user's liked media view"""

    context = {}
    return render(request, "core/liked_media.html", context)


@login_required
def manage_users(request):
    """List users management view"""

    context = {}
    return render(request, "core/manage_users.html", context)


@login_required
def manage_media(request):
    """List media management view"""

    context = {}
    return render(request, "core/manage_media.html", context)


@login_required
def manage_comments(request):
    """List comments management view"""

    context = {}
    return render(request, "core/manage_comments.html", context)


def members(request):
    """List members view"""

    context = {}
    return render(request, "core/members.html", context)


def recommended_media(request):
    """List recommended media view"""

    context = {}
    return render(request, "core/recommended-media.html", context)


def search(request):
    """Search view"""

    context = {}
    RSS_URL = f"/rss{request.environ['REQUEST_URI']}"
    context["RSS_URL"] = RSS_URL
    return render(request, "core/search.html", context)


def tags(request):
    """List tags view"""

    context = {}
    return render(request, "core/tags.html", context)


def tos(request):
    """Terms of service view"""

    context = {}
    return render(request, "core/tos.html", context)


def upload_media(request):
    """Upload media view"""

    from allauth.account.forms import LoginForm

    form = LoginForm()
    context = {}
    context["form"] = form
    context["can_add"] = user_allowed_to_upload(request)
    can_upload_exp = settings.CANNOT_ADD_MEDIA_MESSAGE
    context["can_upload_exp"] = can_upload_exp

    return render(request, "core/add-media.html", context)


def view_media(request):
    """View media view"""

    friendly_token = request.GET.get("m", "").strip()
    context = {}
    media = Media.objects.filter(friendly_token=friendly_token).first()
    if not media:
        context["media"] = None
        return render(request, "core/media.html", context)

    user_or_session = get_user_or_session(request)
    save_user_action.delay(
        user_or_session, friendly_token=friendly_token, action="watch")
    context = {}
    context["media"] = friendly_token
    context["media_object"] = media

    context["CAN_DELETE_MEDIA"] = False
    context["CAN_EDIT_MEDIA"] = False
    context["CAN_DELETE_COMMENTS"] = False

    if request.user.is_authenticated:
        if (media.user.id == request.user.id) or is_mediauploadx_editor(request.user) or is_mediauploadx_manager(request.user):
            context["CAN_DELETE_MEDIA"] = True
            context["CAN_EDIT_MEDIA"] = True
            context["CAN_DELETE_COMMENTS"] = True
    return render(request, "core/media.html", context)


def view_playlist(request, friendly_token):
    """View playlist view"""

    try:
        playlist = Playlist.objects.get(friendly_token=friendly_token)
    except BaseException:
        playlist = None

    context = {}
    context["playlist"] = playlist
    return render(request, "core/playlist.html", context)
