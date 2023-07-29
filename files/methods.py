from django.conf import settings

def is_mediauploadx_manager(user):
    manager=False

    try:
        if user.is_manager or user.is_superuser:
            manager=True
    except BaseException:
        pass
    return manager

def is_mediauploadx_editor(user):
    editor=False

    try:
        if user.is_editor or user.is_superuser:
            editor=True
    except BaseException:
        pass
    return editor


def get_next_state(user, current_state, next_state):
    """Return valid state, given a current and next state
    and the user object.
    Users may themselves perform only allowed transitions
    """

    if next_state not in ["public", "private", "unlisted"]:
        next_state = settings.PORTAL_WORKFLOW  # get default state
    if is_mediauploadx_editor(user):
        # allow any transition
        return next_state

    if settings.PORTAL_WORKFLOW == "private":
        next_state = "private"

    if settings.PORTAL_WORKFLOW == "unlisted":
        # don't allow to make media public in this case
        if next_state == "public":
            next_state = current_state

    return next_state