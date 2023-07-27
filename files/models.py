from django.db import models
from django.conf import settings

from . import helpers

# this is used by Media and Encoding models
# reflects media encoding status for objects
MEDIA_ENCODING_STATUS = (
    ("pending", "Pending"),
    ("running", "Running"),
    ("fail", "Fail"),
    ("success", "Success"),
)

# the media state of a Media object
# this is set by default according to the portal workflow
MEDIA_STATES = (
    ("private", "Private"),
    ("public", "Public"),
    ("unlisted", "Unlisted"),
)

# each uploaded Media gets a media_type hint
# by helpers.get_file_type

MEDIA_TYPES_SUPPORTED = (
    ("video", "Video"),
    ("image", "Image"),
    ("pdf", "Pdf"),
    ("audio", "Audio"),
)

ENCODE_EXTENSIONS = (
    ("mp4", "mp4"),
    ("webm", "webm"),
    ("gif", "gif"),
)

ENCODE_RESOLUTIONS = (
    (2160, "2160"),
    (1440, "1440"),
    (1080, "1080"),
    (720, "720"),
    (480, "480"),
    (360, "360"),
    (240, "240"),
)

CODECS = (
    ("h265", "h265"),
    ("h264", "h264"),
    ("vp9", "vp9"),
)

ENCODE_EXTENSIONS_KEYS = [extension for extension, name in ENCODE_EXTENSIONS]
ENCODE_RESOLUTIONS_KEYS = [
    resolution for resolution, name in ENCODE_RESOLUTIONS]


def original_media_file_path(instance, filename):
    """Helper function to place original media file"""
    file_name = "{0}.{1}".format(
        instance.uid.hex, helpers.get_file_name(filename))
    return settings.MEDIA_UPLOAD_DIR + "user/{0}/{1}".format(instance.user.username, file_name)


def encoding_media_file_path(instance, filename):
    """Helper function to place encoded media file"""

    file_name = "{0}.{1}".format(
        instance.media.uid.hex, helpers.get_file_name(filename))
    return settings.MEDIA_ENCODING_DIR + "{0}/{1}/{2}".format(instance.profile.id, instance.media.user.username, file_name)


def original_thumbnail_file_path(instance, filename):
    """Helper function to place original media thumbnail file"""

    return settings.THUMBNAIL_UPLOAD_DIR + "user/{0}/{1}".format(instance.user.username, filename)


def subtitles_file_path(instance, filename):
    """Helper function to place subtitle file"""

    return settings.SUBTITLES_UPLOAD_DIR + "user/{0}/{1}".format(instance.media.user.username, filename)


def category_thumb_path(instance, filename):
    """Helper function to place category thumbnail file"""

    file_name = "{0}.{1}".format(
        instance.uid.hex, helpers.get_file_name(filename))
    return settings.MEDIA_UPLOAD_DIR + "categories/{0}".format(file_name)




