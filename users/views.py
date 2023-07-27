from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from . models import User, Channel
from . forms import UserForm, ChannelForm
from files.methods import is_mediauploadx_manager, is_mediauploadx_editor


# Utility function
def get_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def view_user(request, username):
    context = {}
    user = get_user(username=username)
    if not user:
        return HttpResponseRedirect("/members")
    context["user"] = user
    context["CAN_EDIT"] = True if (
        (user and user == request.user) or is_mediauploadx_manager(request.user)) else False
    context["CAN_DELETE"] = True if is_mediauploadx_manager(
        request.user) else False
    context["SHOW_CONTACT_FORM"] = True if (
        user.allow_contact or is_mediauploadx_editor(request.user)) else False
    return render(request, "core/user.html", context)


def view_user_media(request, username):
    context = {}
    user = get_user(username=username)
    if not user:
        return HttpResponseRedirect("/members")

    context["user"] = user
    context["user"] = user
    context["CAN_EDIT"] = True if (
        (user and user == request.user) or is_mediauploadx_manager(request.user)) else False
    context["CAN_DELETE"] = True if is_mediauploadx_manager(
        request.user) else False
    context["SHOW_CONTACT_FORM"] = True if (
        user.allow_contact or is_mediauploadx_editor(request.user)) else False
    return render(request, "core/user_media.html", context)


def view_user_playlist(request, username):
    context = {}
    user = get_user(username=username)
    if not user:
        return HttpResponseRedirect("/members")

    context["user"] = user
    context["user"] = user
    context["CAN_EDIT"] = True if (
        (user and user == request.user) or is_mediauploadx_manager(request.user)) else False
    context["CAN_DELETE"] = True if is_mediauploadx_manager(
        request.user) else False
    context["SHOW_CONTACT_FORM"] = True if (
        user.allow_contact or is_mediauploadx_editor(request.user)) else False
    return render(request, "core/user_playlists.html", context)


def view_user_playlist(request, username):
    context = {}
    user = get_user(username=username)
    if not user:
        return HttpResponseRedirect("/members")

    context["user"] = user
    context["CAN_EDIT"] = True if (
        (user and user == request.user) or is_mediauploadx_manager(request.user)) else False
    context["CAN_DELETE"] = True if is_mediauploadx_manager(
        request.user) else False
    context["SHOW_CONTACT_FORM"] = True if (
        user.allow_contact or is_mediauploadx_editor(request.user)) else False

    return render(request, "core/user_about.html", context)


@login_required
def edit_user(request, username):
    user = get_user(username=username)
    if not user or (user != request.user and not is_mediauploadx_manager(request.user)):
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = UserForm(request.user, request.POST,
                        request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = UserForm(request.user, instance=user)
    return render(request, "core/user_edit.html", {"form": form})


def view_channel(request, friendly_token):
    context = {}
    channel = Channel.objects.filter(friendly_token=friendly_token).first()
    if not channel:
        user = None
    else:
        user = channel.user
    context["user"] = user
    context["CAN_EDIT"] = True if (
        (user and user == request.user) or is_mediauploadx_manager(request.user)) else False
    return render(request, "core/channel.html", context)


@login_required
def edit_channel(request, friendly_token):
    channel = Channel.objects.filter(friendly_token=friendly_token).first()
    if not (channel and request.user.is_authenticated and (request.user == channel.user)):
        return HttpResponseRedirect("/")

    if request.method == "POST":
        form = ChannelForm(request.POST, request.FILES, instance=channel)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.save()
            return HttpResponseRedirect(request.user.get_absolute_url())
    else:
        form = ChannelForm(instance=channel)
    return render(request, "core/channel_edit.html", {"form": form})
