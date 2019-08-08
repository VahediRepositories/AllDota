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

    @property
    def radiant_strength_heroes(self):
        return HeroPage.objects.live().filter(
            hero__type__name='Strength',
            hero__ego='Radiant'
        )

    @property
    def dire_strength_heroes(self):
        return HeroPage.objects.live().filter(
            hero__type__name='Strength',
            hero__ego='Dire'
        )

    @property
    def radiant_agility_heroes(self):
        return HeroPage.objects.live().filter(
            hero__type__name='Agility',
            hero__ego='Radiant'
        )

    @property
    def dire_agility_heroes(self):
        return HeroPage.objects.live().filter(
            hero__type__name='Agility',
            hero__ego='Dire'
        )

    @property
    def radiant_intelligence_heroes(self):
        return HeroPage.objects.live().filter(
            hero__type__name='Intelligence',
            hero__ego='Radiant'
        )

    @property
    def dire_intelligence_heroes(self):
        return HeroPage.objects.live().filter(
            hero__type__name='Intelligence',
            hero__ego='Dire'
        )

    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.HeroPage']

    def get_home_page(self):
        return self.get_parent()

    @property
    def template(self):
        return self.get_language_template()

    def clean(self):
        super().clean()
        self.title = 'Heroes'
        self.slug = slugify(self.title)

    def serve(self, request, *args, **kwargs):
        language = translation.get_language()
        if language == 'fa':
            self.search_description = 'تمام هيرو هاى دوتا 2'
            self.seo_title = '{} - {}'.format('تمام هيرو هاى دوتا', 'All Dota2 Heroes')
        else:
            self.search_description = 'Every thing you need to know about Dota2 Heroes.'
            self.seo_title = 'All Dota2 Heroes'
        return super().serve(request, *args, **kwargs)


class HeroPage(MetadataPageMixin, HeroesPageMixin, MultilingualPageMixin, Page):
    hero = models.OneToOneField(
        Hero, on_delete=models.SET_NULL, blank=False, null=True
    )

    content_panels = [
        SnippetChooserPanel('hero'),
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
