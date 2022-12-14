from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from .utilities import get_timestamp_path, send_new_comment_notification


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='is activated?')
    send_messages = models.BooleanField(default=True, verbose_name='Are you need notification about new comments?')

    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='name')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='order')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name='Super rubric')


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Super rubric'
        verbose_name_plural = 'Super rubrics'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Subrubric'
        verbose_name_plural = 'Subrubrics'


class Bb(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='rubric')
    title = models.CharField(max_length=40)
    content = models.TextField()
    price = models.IntegerField(default=0)
    contacts = models.TextField()
    image = models.ImageField(blank=True, upload_to=get_timestamp_path)
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='is active?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Advertisements'
        verbose_name = 'Advertisement'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Advertisement')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Image')

    class Meta:
        verbose_name_plural = 'additional images'
        verbose_name = 'additional image'


class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Advertisement')
    author = models.CharField(max_length=30, verbose_name="Author")
    content = models.TextField(verbose_name='content')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='show?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')

    class Meta:
        verbose_name_plural = 'Comments'
        verbose_name = 'Comment'
        ordering = ['created_at']


def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].bb.author
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(kwargs['instance'])


post_save.connect(post_save_dispatcher, sender=Comment)
