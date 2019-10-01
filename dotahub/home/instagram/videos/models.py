from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.blocks import CharBlock
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtailvideos.models import Video

from . import serializers


@register_snippet
class SimpleVideo(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='+', null=True,
        on_delete=models.SET_NULL
    )
    caption = models.TextField(default='')

    farsi_label = models.TextField(default='')
    english_label = models.TextField(default='')

    panels = [
        FieldPanel('caption'),
        VideoChooserPanel('video'),
        FieldPanel('farsi_label'),
        FieldPanel('english_label'),
    ]

    api_fields = [
        APIField('video', serializer=serializers.VideoField()),
        APIField('caption'),
        APIField('farsi_label'),
        APIField('english_label'),
    ]

    def __str__(self):
        return self.video.title

    class Meta:
        verbose_name_plural = 'Simple Videos'
