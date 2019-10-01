from django.utils.text import slugify
from wagtail.core.models import Page
from wagtailmetadata.models import MetadataPageMixin

from .heroes.blocks import *
from .heroes.models import *
from .instagram.videos.models import *
from .introduction.blocks import *
from .logo.models import *
from .multilingual.models import *


class HomePage(LogoContainingPageMixin, Page):
    subpage_types = [
        'home.HeroesPage',
        'home.Dota2IntroductionPage',
    ]


class HeroesPage(LogoContainingPageMixin, MetadataPageMixin, HeroesPageMixin, MultilingualPageMixin, Page):

    @property
    def radiant_strength_heroes(self):
        return HeroPage.objects.live().filter(
            hero__hero_type__name='Strength',
            hero__ego='Radiant'
        )

    @property
    def dire_strength_heroes(self):
        return HeroPage.objects.live().filter(
            hero__hero_type__name='Strength',
            hero__ego='Dire'
        )

    @property
    def radiant_agility_heroes(self):
        return HeroPage.objects.live().filter(
            hero__hero_type__name='Agility',
            hero__ego='Radiant'
        )

    @property
    def dire_agility_heroes(self):
        return HeroPage.objects.live().filter(
            hero__hero_type__name='Agility',
            hero__ego='Dire'
        )

    @property
    def radiant_intelligence_heroes(self):
        return HeroPage.objects.live().filter(
            hero__hero_type__name='Intelligence',
            hero__ego='Radiant'
        )

    @property
    def dire_intelligence_heroes(self):
        return HeroPage.objects.live().filter(
            hero__hero_type__name='Intelligence',
            hero__ego='Dire'
        )

    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.HeroPage']

    def get_home_page(self):
        return self.get_parent()

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

    @property
    def template(self):
        return super().template

    @property
    def farsi_translated(self):
        return True

    @property
    def english_translated(self):
        return True


class HeroPage(LogoContainingPageMixin, MetadataPageMixin, HeroesPageMixin, MultilingualPageMixin, Page):
    hero = models.OneToOneField(
        Hero, on_delete=models.SET_NULL, blank=False, null=True
    )

    content_panels = [
        SnippetChooserPanel('hero'),
    ]

    promote_panels = []
    settings_panels = []

    @property
    def farsi_url(self):
        return super().get_farsi_url()

    @property
    def english_url(self):
        return super().get_english_url()

    api_fields = [
        APIField('hero'),
        APIField('farsi_url'),
        APIField('english_url'),
    ]

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
        return super().template

    @property
    def farsi_translated(self):
        return self.hero.farsi_translated

    @property
    def english_translated(self):
        return self.hero.english_translated


class Dota2IntroductionPage(LogoContainingPageMixin, MetadataPageMixin, MultilingualPageMixin, Page):
    sections = StreamField(
        [
            ('section', IntroductionSection())
        ], null=True, blank=True
    )

    farsi_translated = models.BooleanField(default=False)
    english_translated = models.BooleanField(default=False)

    content_panels = [
        MultiFieldPanel(
            [
                StreamFieldPanel('sections'),
            ], heading='sections', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('farsi_translated'),
                FieldPanel('english_translated')
            ], heading='Translations', classname='collapsible collapsed'
        )
    ]

    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.HomePage']
    subpage_types = []

    def serve(self, request, *args, **kwargs):
        language = translation.get_language()
        if language == 'fa':
            self.search_description = 'محبوب ترين بازى استيم. هر روز ميليون ها بازيكن از سراسر جهان، با انتخاب يكى از هيروها وارد نبرد ميشوند. مهم نيست مبتدى باشيد يا حرفه اى. هميشه چيزى براى كشف كردن هست.'
            self.seo_title = 'Dota2 - رايگان بازى كنيد'
        else:
            self.search_description = "The most-played game on Steam. Every day, millions of players worldwide enter battle as one of over a hundred Dota heroes. And no matter if it's their 10th hour of play or 1,000th, there's always something new to discover."
            self.seo_title = 'Dota2 - Play for Free'
        return super().serve(request, *args, **kwargs)

    def clean(self):
        super().clean()
        self.title = 'Dota2 Introduction'
        self.slug = slugify(self.title)

    def get_home_page(self):
        return self.get_parent()

    @property
    def template(self):
        return super().template
