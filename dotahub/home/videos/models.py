import cv2
from django.conf import settings
from django.core.files import File
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.snippets.models import register_snippet
from wagtailvideos.edit_handlers import VideoChooserPanel
from wagtailvideos.models import Video

from . import serializers


class SimpleVideoEnglishTag(TaggedItemBase):
    content_object = models.ForeignKey(
        'SimpleVideo', related_name='tagged_items', on_delete=models.CASCADE
    )


class SimpleVideoFarsiTag(TaggedItemBase):
    content_object = models.ForeignKey(
        'SimpleVideo', related_name='simple_video_farsi_tags', on_delete=models.CASCADE
    )


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

    english_tags = ClusterTaggableManager(
        through=SimpleVideoEnglishTag, blank=True
    )
    # farsi_tags = ClusterTaggableManager(
    #     through=SimpleVideoFarsiTag, blank=True, related_name='farsi_tags'
    # )

    panels = [
        MultiFieldPanel(
            [
                VideoChooserPanel('video'),
                FieldPanel('caption'),
                FieldPanel('farsi_label'),
                FieldPanel('english_label'),
            ], heading='details', classname='collapsible collapsed'
        ),

        MultiFieldPanel(
            [
                FieldPanel('english_tags'),
            ], heading='english_tags', classname='collapsible collapsed'
        ),
        # MultiFieldPanel(
        #     [
        #         FieldPanel('farsi_tags'),
        #     ], heading='farsi_tags', classname='collapsible collapsed'
        # )
    ]

    api_fields = [
        APIField('video', serializer=serializers.VideoField()),
        APIField('caption'),
        APIField('farsi_label'),
        APIField('english_label'),
    ]

    def save(self, *args, **kwargs):
        if not self.video.thumbnail:
            video = cv2.VideoCapture(self.video.file.path)
            ret, frame = video.read()
            path = settings.MEDIA_ROOT + '/original_images/video_{}_thumbnail.png'.format(
                self.video.pk
            )
            cv2.imwrite(path, frame)
            video.release()
            cv2.destroyAllWindows()
            file = File(open(path, 'rb'))
            self.video.thumbnail.save(
                path, file, True
            )
        super(SimpleVideo, self).save()

    def __str__(self):
        return self.video.title

    class Meta:
        verbose_name_plural = 'Simple Videos'
