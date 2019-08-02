from django.utils.text import slugify
from wagtail.core.models import Page
from wagtailmetadata.models import MetadataPageMixin

from .heroes.blocks import *
from .heroes.models import *
from .multilingual.models import *


class HomePage(Page):
    subpage_types = [
        'home.HeroesPage'
    ]


class HeroesPage(MetadataPageMixin, HeroesPageMixin, MultilingualPageMixin, Page):
    promote_panels = Page.promote_panels + MetadataPageMixin.panels

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.HeroPage']

    @property
    def template(self):
        return self.get_language_template()

    def get_home_page(self):
        return self.get_parent()


class HeroPage(MetadataPageMixin, HeroesPageMixin, MultilingualPageMixin, Page):
    hero = models.OneToOneField(
        Hero, on_delete=models.SET_NULL, blank=False, null=True
    )

    abilities = StreamField(
        [
            ('ability', HeroAbility())
        ], null=True, blank=True
    )

    content_panels = [
        SnippetChooserPanel('hero'),
        StreamFieldPanel('abilities'),
    ]

    promote_panels = []
    settings_panels = []

    def get_home_page(self):
        return self.get_parent().specific.get_home_page()

    parent_page_types = ['home.HeroesPage']
    subpage_types = []

    def serve(self, request, *args, **kwargs):
        language = translation.get_language()
        if language == 'fa':
            self.search_description = 'هر آنچه كه در مورد {} در دوتا بايد بدانيد. شامل مطالب آموزشى، تمام قابليت ها و جديد ترين تغييرات'.format(
                self.hero.farsi_name
            )
            self.seo_title = '{} - {} - {} - {} - {}'.format(
                self.hero.name, self.hero.farsi_name,
                'Hero', 'هيرو', 'Dota2'
            )
        else:
            self.search_description = 'Every thing you need to know about Dota2 Hero named {}.'.format(
                self.hero.name
            )
            self.seo_title = '{} - Hero - Dota2'.format(self.hero.name)
        return super().serve(request, *args, **kwargs)

    def clean(self):
        super().clean()
        self.title = self.hero.name
        self.slug = slugify(self.title)
        self.search_image = self.hero.horizontal_image

    @property
    def template(self):
        return self.get_language_template()
