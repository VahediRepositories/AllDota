from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, RichTextFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.snippets.models import register_snippet

from ..modules import text_processing
from .. import configurations
from ..blogs.blocks import SectionBlock


@register_snippet
class BlogPost(models.Model):
    post_title = RichTextField(
        features=[], blank=False, null=True,
    )
    post_summary = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=False, null=True,
    )
    post_introduction = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=True, null=True,
    )
    post_conclusion = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=True, null=True,
    )
    sections = StreamField(
        [
            ('section', SectionBlock()),
        ], blank=False
    )

    panels = [
        MultiFieldPanel(
            [
                RichTextFieldPanel('post_title'),
                RichTextFieldPanel('post_summary'),
                RichTextFieldPanel('post_introduction'),
                StreamFieldPanel('sections'),
                RichTextFieldPanel('post_conclusion'),
            ], heading='Post Content'
        ),
    ]

    @property
    def sections_with_title(self):
        sections = []
        for section in self.sections:
            if section.value['title']:
                sections.append(section)
        return sections

    def __str__(self):
        return text_processing.html_to_str(
            self.post_title
        )
