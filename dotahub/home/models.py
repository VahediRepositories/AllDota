import os
import uuid

import cv2
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.text import slugify
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import RichTextFieldPanel
from wagtail.core.models import Page
from wagtail.images.models import Image
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtailmetadata.models import MetadataPageMixin

from .modules import list_processing
from .heroes.blocks import *
from .heroes.models import *
from .introduction.blocks import *
from .logo.models import *
from .multilingual.models import *


class AllDotaPageMixin:

    @staticmethod
    def get_home_page():
        return HomePage.objects.first()


class HomePage(AllDotaPageMixin, LogoContainingPageMixin, Page):
    subpage_types = [
        'home.HeroesPage',
        'home.Dota2IntroductionPage',
        'home.ShortVideosPage',
    ]


class HeroesPage(
    AllDotaPageMixin, LogoContainingPageMixin,
    MetadataPageMixin, HeroesPageMixin, MultilingualPageMixin, Page
):

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

    content_panels = []
    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.HeroPage']

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


class HeroPage(
    AllDotaPageMixin, LogoContainingPageMixin,
    MetadataPageMixin, HeroesPageMixin, MultilingualPageMixin, Page
):
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
        if self.hero:
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


class Dota2IntroductionPage(
    AllDotaPageMixin, LogoContainingPageMixin,
    MetadataPageMixin, MultilingualPageMixin, Page
):
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

    @property
    def template(self):
        return super().template


class ShortVideoPageEnglishTag(TaggedItemBase):
    content_object = ParentalKey(
        'ShortVideoPage', related_name='short_video_page_english_tags'
    )


class ShortVideoPageFarsiTag(TaggedItemBase):
    content_object = ParentalKey(
        'ShortVideoPage', related_name='short_video_page_farsi_tags'
    )


class ShortVideoPage(
    AllDotaPageMixin, LogoContainingPageMixin,
    MetadataPageMixin, MultilingualPageMixin, Page
):
    video = models.ForeignKey(
        'wagtailmedia.Media',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    video_thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )

    @property
    def thumbnail(self):
        if self.video_thumbnail:
            return self.video_thumbnail
        else:
            return self.update_thumbnail()

    def update_thumbnail(self):
        generated_file = False
        if self.video.thumbnail:
            file = open(self.video.thumbnail.path, 'rb')
            file = File(file)
        else:
            clip = cv2.VideoCapture(self.video.file.path)
            ret, frame = clip.read()
            generated_file = 'thumbnail.jpeg'
            cv2.imwrite(generated_file, frame)
            file = open(generated_file, 'rb')
            file = File(file)
        thumbnail = Image(
            title=text_processing.html_to_str(
                self.english_title
            ), file=file
        )
        thumbnail.save()
        self.video_thumbnail = thumbnail
        self.save()
        if generated_file:
            os.remove(generated_file)
        return thumbnail

    english_title = RichTextField(
        features=[], blank=False, null=True
    )

    farsi_title = RichTextField(
        features=[], blank=False, null=True,
        help_text='It has to start with a farsi word'
    )

    english_caption = RichTextField(
        features=[], blank=False, null=True,
    )

    farsi_caption = RichTextField(
        features=[], blank=False, null=True,
        help_text='It has to start with a farsi word'
    )

    english_tags = ClusterTaggableManager(
        through=ShortVideoPageEnglishTag, blank=True, related_name='english_tags'
    )
    farsi_tags = ClusterTaggableManager(
        through=ShortVideoPageFarsiTag, blank=True, related_name='farsi_tags'
    )

    content_panels = [
        MultiFieldPanel(
            [
                MediaChooserPanel('video'),
            ], heading='video', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('farsi_title'),
                RichTextFieldPanel('farsi_caption'),
                FieldPanel('farsi_tags'),
            ], heading='farsi', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('english_title'),
                RichTextFieldPanel('english_caption'),
                FieldPanel('english_tags'),
            ], heading='english', classname='collapsible collapsed'
        ),
    ]
    promote_panels = []
    settings_panels = []

    @property
    def farsi_url(self):
        return super().get_farsi_url()

    @property
    def english_url(self):
        return super().get_english_url()

    @property
    def template(self):
        return super().template

    @property
    def farsi_translated(self):
        return True

    @property
    def english_translated(self):
        return True

    def serve(self, request, *args, **kwargs):
        language = translation.get_language()
        if language == 'fa':
            self.search_description = text_processing.html_to_str(
                self.english_caption
            )
            self.seo_title = text_processing.html_to_str(
                self.english_title
            )
        else:
            self.search_description = text_processing.html_to_str(
                self.farsi_caption
            )
            self.seo_title = text_processing.html_to_str(
                self.farsi_title
            )
        return super().serve(request, *args, **kwargs)

    def clean(self):
        super().clean()
        if self.english_title:
            self.title = text_processing.html_to_str(
                self.english_title
            )
            pages = ShortVideoPage.objects.filter(title=self.title)
            if pages:
                if not self.id:
                    self.set_uuid4()
                    self.slug = slugify(
                        '{}_{}'.format(
                            self.title, self.uuid4
                        )
                    )
                else:
                    self.slug = slugify(
                        '{}_{}'.format(
                            self.title, self.id
                        )
                    )

    uuid4 = models.TextField(default='', blank=True)

    def set_uuid4(self):
        uuid4 = uuid.uuid4()
        while ShortVideoPage.objects.filter(uuid4=uuid4).exists():
            uuid4 = uuid.uuid4()
        self.uuid4 = str(uuid4)

    parent_page_types = ['home.ShortVideosPage']
    subpage_types = []

    def __str__(self):
        return self.english_title


class ShortVideosPage(
    AllDotaPageMixin, LogoContainingPageMixin,
    MetadataPageMixin, HeroesPageMixin, MultilingualPageMixin, Page
):
    content_panels = []
    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.ShortVideoPage']

    def clean(self):
        super().clean()
        self.title = 'Short Videos'
        self.slug = slugify(self.title)

    def serve(self, request, *args, **kwargs):
        language = translation.get_language()
        if language == 'fa':
            self.search_description = 'ويديو هاى كوتاه ديدنى دوتا 2 را اينجا ببينيد'
            self.seo_title = 'ويديو هاى كوتاه دوتا 2'
        else:
            self.search_description = 'Amazing Dota 2 short videos'
            self.seo_title = 'Dota 2 short videos'
        return super().serve(request, *args, **kwargs)

    @staticmethod
    def get_row_posts(posts):
        return list(
            reversed(list_processing.list_to_sublists_of_size_n(posts, 2))
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        children = self.get_children().live().public()
        paginator = Paginator(children, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['row_posts'] = self.get_row_posts(posts)
        context['posts'] = posts
        return context

    @property
    def template(self):
        return super().template

    @property
    def farsi_translated(self):
        return True

    @property
    def english_translated(self):
        return True
