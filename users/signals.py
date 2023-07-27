
from django.core.mail import EmailMessage
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


from . models import User, Channel
from core import settings

@receiver(post_save, sender=User)
def post_user_create(sender, instance, created, **kwargs):
    # create a Channel object upon user creation, name it default
    if created:
        new = Channel.objects.create(title="default", user=instance)
        new.save()
        if settings.ADMINS_NOTIFICATIONS.get("NEW_USER", False):
            title = "[{}] - New user just registered".format(
                settings.PORTAL_NAME)
            msg = """
User has just registered with email %s\n
Visit user profile page at %s
            """ % (
                instance.email,
                settings.SSL_FRONTEND_HOST + instance.get_absolute_url(),
            )
            email = EmailMessage(
                title, msg, settings.DEFAULT_FROM_EMAIL, settings.ADMIN_EMAIL_LIST)
            email.send(fail_silently=True)

# @receiver(post_delete, sender=User)
# def delete_content(sender, instance, **kwargs):
#     """Delete user related content
#     Upon user deletion
#     """

#     Media.objects.filter(user=instance).delete()
#     Tag.objects.filter(user=instance).delete()
#     Category.objects.filter(user=instance).delete()
