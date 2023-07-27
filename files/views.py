from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . methods import is_mediauploadx_editor, is_mediauploadx_manager


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
    return render(request, "cms/add_subtitle.html", {"form": form})
