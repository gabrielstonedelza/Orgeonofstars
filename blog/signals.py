from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import NotifyMe, Report, Post, Comments


@receiver(post_save, sender=Report)
def create_report(sender, created, instance, **kwargs):
    title = "New Report"
    message = f"{instance.user.username} add a new report"

    admin_user = get_object_or_404(User, username="joselyn")

    if created:
        NotifyMe.objects.create(user=admin_user, notify_title=title,
                                notify_alert=message, sender=instance.user, greport=instance.id)


@receiver(post_save, sender=Post)
def alert_post_create(sender, created, instance, **kwargs):
    title = "New Post"
    message = f"{instance.author.username} added a new post"

    users = User.objects.exclude(id=instance.author.id)

    if created:
        for i in users:
            NotifyMe.objects.create(user=i, notify_title=title, notify_alert=message,
                                    sender=instance.author, gpost=instance.id)


@receiver(post_save, sender=Comments)
def alert_post_comment(sender, created, instance, **kwargs):
    title = "New post comment"
    post_user = instance.post.author
    message = f"{instance.user.username} comment on your post '{instance.post.title}"

    if created:
        if not instance.user == instance.post.author:
            NotifyMe.objects.create(user=post_user, notify_title=title, notify_alert=message,
                                    sender=instance.user, gpost=instance.post.id)
