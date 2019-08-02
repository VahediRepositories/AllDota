import re

from django.db import models
from django.utils import translation
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class MultilingualPageMixin:

    @staticmethod
    def convert(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @property
    def farsi_template(self):
        return 'home/fa/' + self.convert(self.__class__.__name__) + '.html'

    @property
    def english_template(self):
        return 'home/en/' + self.convert(self.__class__.__name__) + '.html'

    def get_language_template(self):
        language = translation.get_language()
        if language == 'fa':
            return self.farsi_template
        else:
            return self.english_template

    def get_language_url(self, lang):
        current_lang = translation.get_language()
        translation.activate(lang)
        url = self.get_url()
        translation.activate(current_lang)
        return url

    def get_farsi_url(self):
        return self.get_language_url('fa')

    def get_english_url(self):
        return self.get_language_url('en')

    @staticmethod
    def get_farsi_image():
        return Language.objects.get(name='Persian').flag

    @staticmethod
    def get_english_image():
        return Language.objects.get(name='English').flag


@register_snippet
class Language(models.Model):
    name = models.CharField(max_length=60, unique=True)
    farsi_name = models.CharField(max_length=60, unique=True)
    flag = models.ForeignKey(
        'wagtailimages.Image',
        help_text='horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'), FieldPanel('farsi_name'), ImageChooserPanel('flag')
    ]

    def __str__(self):
        return self.name