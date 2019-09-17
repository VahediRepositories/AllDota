from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class LogoContainingPageMixin:

    @property
    def logo_image_light(self):
        return self.logo.logo_image_light

    @property
    def logo_image_dark(self):
        return self.logo.logo_image_dark

    @property
    def logo_text_light(self):
        return self.logo.text_image_light

    @property
    def logo_text_dark(self):
        return self.logo.text_image_dark

    @property
    def first_logo(self):
        return Logo.objects.first()

    @property
    def logo(self):
        logo_object = Logo.objects.filter(enabled=True).first()
        if logo_object:
            return logo_object
        else:
            return self.first_logo


@register_snippet
class Logo(models.Model):
    logo_image_light = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    logo_image_dark = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    text_image_light = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    text_image_dark = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    enabled = models.BooleanField(default=False)

    panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('logo_image_dark'),
                ImageChooserPanel('text_image_dark'),
            ], heading='Dark', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('logo_image_light'),
                ImageChooserPanel('text_image_light'),
            ], heading='Light', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('enabled'),
            ], heading='Settings', classname='collapsible collapsed'
        ),

    ]

    def __str__(self):
        return 'Logo-{}'.format(self.pk)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.enabled:
            other_logos = Logo.objects.all().exclude(pk=self.pk)
            for logo in other_logos:
                logo.enabled = False
                logo.save()
