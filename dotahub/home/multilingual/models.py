import re

from django.db import models
from django.utils import translation
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class MultilingualPageMixin:

    @property
    def template(self):
        lang = translation.get_language()
        if lang == 'fa':
            if self.farsi_translated:
                return self.farsi_template
            elif self.english_translated:
                return self.english_template
        elif lang == 'en':
            if self.english_translated:
                return self.english_template
            elif self.farsi_translated:
                return self.farsi_template

    @property
    def language(self):
        return translation.get_language()

    def get_farsi_url(self):
        return self.get_language_url('fa')

    def get_english_url(self):
        return self.get_language_url('en')

    @staticmethod
    def get_farsi_language():
        return Language.objects.get(name='Persian')

    @staticmethod
    def get_english_language():
        return Language.objects.get(name='English')

    @property
    def template_language(self):
        lang = translation.get_language()
        if lang == 'fa':
            if self.farsi_translated:
                return 'fa'
            elif self.english_translated:
                return 'en'
        elif lang == 'en':
            if self.english_translated:
                return 'en'
            elif self.farsi_translated:
                return 'fa'

    @property
    def template_language_dir(self):
        if self.template_language == 'fa':
            return 'rtl'
        elif self.template_language == 'en':
            return 'ltr'

    @property
    def farsi_template(self):
        return 'home/fa/' + self.template_file

    @property
    def english_template(self):
        return 'home/en/' + self.template_file

    @property
    def template_name(self):
        return self.convert(self.__class__.__name__)

    @property
    def template_file(self):
        return self.template_name + '.html'

    def get_language_url(self, lang):
        current_lang = translation.get_language()
        translation.activate(lang)
        url = self.get_url()
        translation.activate(current_lang)
        return url

    @staticmethod
    def convert(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


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
