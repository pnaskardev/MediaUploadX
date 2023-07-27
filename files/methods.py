

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