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

from .blogs.models import BlogPost
from .modules import list_processing
from .heroes.blocks import *
from .heroes.models import *
from .blogs.blocks import *
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
        'home.ShortPostsPage',
        'home.BlogsPage',
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
            self.search_description = 'Amazing Dota 2 short short_videos'
            self.seo_title = 'Dota 2 short short_videos'
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


class ShortPostPageEnglishTag(TaggedItemBase):
    content_object = ParentalKey(
        'ShortPostPage', related_name='short_post_page_english_tags'
    )


class ShortPostPageFarsiTag(TaggedItemBase):
    content_object = ParentalKey(
        'ShortPostPage', related_name='short_post_page_farsi_tags'
    )


class ShortPostPage(
    AllDotaPageMixin, LogoContainingPageMixin,
    MetadataPageMixin, MultilingualPageMixin, Page
):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    english_caption = RichTextField(
        features=[], blank=False, null=True,
    )

    farsi_caption = RichTextField(
        features=[], blank=False, null=True,
        help_text='It has to start with a farsi word'
    )

    english_tags = ClusterTaggableManager(
        through=ShortPostPageEnglishTag, blank=True, related_name='short_post_english_tags'
    )
    farsi_tags = ClusterTaggableManager(
        through=ShortPostPageFarsiTag, blank=True, related_name='short_post_farsi_tags'
    )

    content_panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('image')
            ], heading='image', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                RichTextFieldPanel('farsi_caption'),
                FieldPanel('farsi_tags'),
            ], heading='farsi', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
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
        if language == 'en':
            self.search_description = text_processing.html_to_str(
                self.english_caption
            )
            self.seo_title = self.title
        else:
            self.search_description = text_processing.html_to_str(
                self.farsi_caption
            )
            self.seo_title = self.title
        return super().serve(request, *args, **kwargs)

    def clean(self):
        super().clean()
        if self.image and self.image.title:
            self.title = self.image.title
            pages = ShortPostPage.objects.filter(title=self.title)
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

    parent_page_types = [
        'home.ShortPostsPage',
    ]
    subpage_types = []

    def __str__(self):
        return self.english_title


class ShortPostsPage(
    AllDotaPageMixin, LogoContainingPageMixin,
    MetadataPageMixin, MultilingualPageMixin, Page
):
    content_panels = []
    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.HomePage']
    subpage_types = ['home.ShortPostPage']

    def clean(self):
        super().clean()
        self.title = 'Short Posts'
        self.slug = slugify(self.title)

    def serve(self, request, *args, **kwargs):
        language = translation.get_language()
        if language == 'fa':
            self.search_description = 'مطالب كوتاه درباره ى دوتا 2 (Dota2)'
            self.seo_title = self.search_description
        else:
            self.search_description = 'Dota 2 short posts'
            self.seo_title = self.search_description
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


class BlogsPage(
    AllDotaPageMixin, LogoContainingPageMixin,
    MetadataPageMixin, MultilingualPageMixin, Page
):
    content_panels = []
    promote_panels = []
    settings_panels = []

    parent_page_types = ['home.HomePage']
    subpage_types = [
        'home.AllDotaBlogPost1',
    ]

    def clean(self):
        super().clean()
        self.title = 'Blogs'
        self.slug = slugify(self.title)

    def serve(self, request, *args, **kwargs):
        language = translation.get_language()
        if language == 'fa':
            self.seo_title = 'وبلاگ آلدوتا'
            self.search_description = self.seo_title + ' شامل عكس ها، ويديو ها و پست هاى دوتا 2 (DOTA 2)'
        else:
            self.seo_title = 'AllDota Blogs'
            self.search_description = self.seo_title + ' including images, videos, posts about Dota 2'
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


class AllDotaBlogPost1FarsiTag(TaggedItemBase):
    content_object = ParentalKey(
        'AllDotaBlogPost1', related_name='blog_post1_farsi_tags', on_delete=models.CASCADE
    )


class AllDotaBlogPost1EnglishTag(TaggedItemBase):
    content_object = ParentalKey(
        'AllDotaBlogPost1', related_name='blog_post1_english_tags', on_delete=models.CASCADE
    )


class AllDotaBlogPost1(
    AllDotaPageMixin, LogoContainingPageMixin, MultilingualPageMixin, MetadataPageMixin, Page
):
    image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    farsi_content = models.ForeignKey(
        BlogPost, blank=True, on_delete=models.SET_NULL, null=True, related_name='farsi_content'
    )
    english_content = models.ForeignKey(
        BlogPost, blank=True, on_delete=models.SET_NULL, null=True, related_name='english_content'
    )
    farsi_tags = ClusterTaggableManager(
        through=AllDotaBlogPost1FarsiTag, blank=True, related_name='post1_farsi_tags'
    )
    english_tags = ClusterTaggableManager(
        through=AllDotaBlogPost1EnglishTag, blank=True, related_name='post1_english_tags'
    )
    farsi_translated = models.BooleanField(default=False, blank=False)
    english_translated = models.BooleanField(default=False, blank=False)

    uuid4 = models.TextField(default='')

    content_panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('image')
            ], heading="Image", classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                SnippetChooserPanel('english_content'),
                FieldPanel('english_tags'),
            ], heading="English", classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                SnippetChooserPanel('farsi_content'),
                FieldPanel('farsi_tags'),
            ], heading="Farsi", classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('farsi_translated'),
                FieldPanel('english_translated'),
            ], heading='Translation', classname='collapsible collapsed'
        ),
    ]

    promote_panels = []
    settings_panels = []

    @property
    def template(self):
        return super().template

    def clean(self):
        super().clean()
        if not self.id:
            self.refresh_slug()
        if self.english_content:
            self.title = text_processing.html_to_str(
                self.english_content.post_title
            )
        elif self.farsi_content:
            self.title = text_processing.html_to_str(
                self.farsi_content.post_title
            )
        else:
            self.title = self.slug
        # self.search_image = self.image

    def refresh_slug(self):
        self.set_uuid4()
        self.slug = '{}-'.format(
            type(self).__name__
        ) + self.uuid4

    def set_english_seo(self):
        self.seo_title = 'Blogs - {}'.format(
            text_processing.html_to_str(
                self.english_content.post_title
            )
        )
        self.search_description = text_processing.html_to_str(
            self.english_content.post_summary
        )

    def set_farsi_seo(self):
        self.seo_title = 'وبلاگ - {}'.format(
            text_processing.html_to_str(
                self.farsi_content.post_title
            )
        )
        self.search_description = text_processing.html_to_str(
            self.farsi_content.post_summary
        )

    def serve(self, request, *args, **kwargs):
        language = translation.get_language()
        if language == 'fa':
            if self.farsi_content:
                self.set_farsi_seo()
            elif self.english_content:
                self.set_english_seo()
        elif language == 'en':
            if self.english_content:
                self.set_english_seo()
            elif self.farsi_content:
                self.set_farsi_seo()
        return super().serve(request, *args, **kwargs)

    def set_uuid4(self):
        uuid4 = uuid.uuid4()
        while AllDotaBlogPost1.objects.filter(uuid4=uuid4).exists():
            uuid4 = uuid.uuid4()
        self.uuid4 = str(uuid4)

    class Meta:
        ordering = [
            '-first_published_at'
        ]

# class BlogPost(AllDotaPageMixin, LogoContainingPageMixin, MetadataPageMixin, Page):
#     post_title = RichTextField(
#         features=[], blank=False, null=True,
#     )
#     post_summary = RichTextField(
#         features=configurations.RICHTEXT_FEATURES, blank=False, null=True,
#     )
#     post_introduction = RichTextField(
#         features=configurations.RICHTEXT_FEATURES, blank=True, null=True,
#     )
#     post_conclusion = RichTextField(
#         features=configurations.RICHTEXT_FEATURES, blank=True, null=True,
#     )
#     sections = StreamField(
#         [
#             ('section', SectionBlock()),
#         ], blank=False
#     )
#
#     @property
#     def sections_with_title(self):
#         sections = []
#         for section in self.sections:
#             if section.value['title']:
#                 sections.append(section)
#         return sections
#
#     def clean(self):
#         super().clean()
#         if not self.id:
#             self.set_uuid4()
#             self.slug = 'post-' + self.uuid4
#         if self.post_title:
#             self.title = text_processing.html_to_str(self.article_title)
#         # self.search_image = self.image
#
#     def set_uuid4(self):
#         uuid4 = uuid.uuid4()
#         while self.manager.filter(uuid4=uuid4).exists():
#             uuid4 = uuid.uuid4()
#         self.uuid4 = str(uuid4)
#
#     uuid4 = models.TextField(default='')
#
#     parent_page_types = ['home.BlogsPage']
#     subpage_types = []
#
#     class Meta:
#         abstract = True
#         ordering = [
#             '-first_published_at'
#         ]
#
#
# class BlogPostType1(BlogPost):
#     image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
#     )
#
#     class Meta:
#         abstract = True
#
#
# class FarsiBlogPost1FarsiTag(TaggedItemBase):
#     content_object = ParentalKey(
#         'FarsiBlogPost1', related_name='farsi_blog_post_farsi_tags', on_delete=models.CASCADE
#     )
#
#
# class FarsiBlogPost1EnglishTag(TaggedItemBase):
#     content_object = ParentalKey(
#         'FarsiBlogPost1', related_name='farsi_blog_post_english_tags', on_delete=models.CASCADE
#     )
#
#
# class FarsiBlogPost1(MultilingualPageMixin, BlogPostType1):
#     farsi_tags = ClusterTaggableManager(
#         through=FarsiBlogPost1FarsiTag, blank=False, related_name='farsi_post_farsi_tags'
#     )
#     english_tags = ClusterTaggableManager(
#         through=FarsiBlogPost1EnglishTag, blank=True, related_name='farsi_post_english_tags'
#     )
#
#     content_panels = [
#         MultiFieldPanel(
#             [
#                 RichTextFieldPanel('post_title'),
#                 ImageChooserPanel('image'),
#             ], heading='Details', classname="collapsible collapsed"
#         ),
#         MultiFieldPanel(
#             [
#                 RichTextFieldPanel('post_summary'),
#                 RichTextFieldPanel('post_introduction'),
#                 StreamFieldPanel('sections'),
#                 RichTextFieldPanel('post_conclusion'),
#             ], heading='Content', classname="collapsible collapsed"
#         ),
#         MultiFieldPanel(
#             [
#                 FieldPanel('farsi_tags'),
#             ], heading='Farsi Tags', classname='collapsible collapsed'
#         ),
#         MultiFieldPanel(
#             [
#                 FieldPanel('english_tags'),
#             ], heading='English Tags', classname='collapsible collapsed'
#         ),
#     ]
#
#     promote_panels = []
#     settings_panels = []
#
#     def serve(self, request, *args, **kwargs):
#         self.search_description = self.title
#         if self.sections_with_title:
#             self.search_description += ' شامل ' + text_processing.str_list_to_comma_separated(
#                 [
#                     text_processing.html_to_str(section.value['title'].source)
#                     for section in self.sections_with_title
#                 ]
#             )
#         self.seo_title = 'وبلاگ - {}'.format(
#             self.title
#         )
#         return super().serve(request, *args, **kwargs)
#
#     @property
#     def manager(self):
#         return FarsiBlogPost1.objects
#
#     @property
#     def farsi_translated(self):
#         return True
#
#     @property
#     def english_translated(self):
#         return False
#
#     @property
#     def template(self):
#         return super().template
#
#
# class EnglishBlogPost1Tag(TaggedItemBase):
#     content_object = ParentalKey(
#         'EnglishBlogPost1', related_name='english_blog_post_tags', on_delete=models.CASCADE
#     )
#
#
# class EnglishBlogPost1(BlogPostType1):
#     tags = ClusterTaggableManager(
#         through=EnglishBlogPost1Tag, blank=False, related_name='english_post_tags'
#     )
#
#     content_panels = [
#         MultiFieldPanel(
#             [
#                 RichTextFieldPanel('post_title'),
#                 ImageChooserPanel('image'),
#             ], heading='Details', classname="collapsible collapsed"
#         ),
#         MultiFieldPanel(
#             [
#                 RichTextFieldPanel('post_summary'),
#                 RichTextFieldPanel('post_introduction'),
#                 StreamFieldPanel('sections'),
#                 RichTextFieldPanel('post_conclusion'),
#             ], heading='Content', classname="collapsible collapsed"
#         ),
#         MultiFieldPanel(
#             [
#                 FieldPanel('tags'),
#             ], heading='Tags', classname='collapsible collapsed'
#         ),
#     ]
#
#     promote_panels = []
#     settings_panels = []
#
#     def serve(self, request, *args, **kwargs):
#         self.search_description = self.title
#         if self.sections_with_title:
#             self.search_description += ' including ' + text_processing.str_list_to_comma_separated(
#                 [
#                     text_processing.html_to_str(section.value['title'].source)
#                     for section in self.sections_with_title
#                 ]
#             )
#         self.seo_title = 'Blogs - {}'.format(
#             self.title
#         )
#         return super().serve(request, *args, **kwargs)
#
#     @property
#     def manager(self):
#         return EnglishBlogPost1.objects
#
#     @property
#     def farsi_translated(self):
#         return False
#
#     @property
#     def english_translated(self):
#         return True
#
#     @property
#     def template(self):
#         return super().template
