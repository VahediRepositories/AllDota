from wagtail.core.models import Page
from wagtailmetadata.models import MetadataPageMixin

from django.utils.text import slugify

from .heroes.blocks import *
from .heroes.models import *


class HomePage(Page):
    subpage_types = [
        'home.HeroesPage'
    ]


class AllDotaPage:
    @staticmethod
    def get_intelligence_image():
        return HeroPropertyImage.objects.all()[0].intelligence

    @staticmethod
    def get_agility_image():
        return HeroPropertyImage.objects.all()[0].agility

    @staticmethod
    def get_strength_image():
        return HeroPropertyImage.objects.all()[0].strength

    @staticmethod
    def get_damage_image():
        return HeroPropertyImage.objects.all()[0].damage

    @staticmethod
    def get_move_speed_image():
        return HeroPropertyImage.objects.all()[0].move_speed

    @staticmethod
    def get_armor_image():
        return HeroPropertyImage.objects.all()[0].armor


class HeroesPage(MetadataPageMixin, AllDotaPage, Page):
    promote_panels = Page.promote_panels + MetadataPageMixin.panels

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.HeroPage']


class HeroPage(MetadataPageMixin, AllDotaPage, Page):
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

    parent_page_types = ['home.HeroesPage']
    subpage_types = []

    def clean(self):
        super().clean()
        self.search_description = 'هر آنچه كه در مورد {} در دوتا بايد بدانيد. شامل مطالب آموزشى، تمام قابليت ها و جديد ترين تغييرات'.format(
            self.hero.farsi_name
        )
        self.seo_title = '{} - {} - {} - {} - {}'.format(
            self.hero.name, self.hero.farsi_name,
            'Hero', 'هيرو', 'Dota2'
        )
        self.title = self.hero.name
        self.slug = slugify(self.title)
