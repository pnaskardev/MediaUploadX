from rest_framework import permissions

from .methods import is_mediauploadx_editor


class IsMediacmsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        if is_mediacms_editor(request.user):
            return True
        return False
