from django import forms
from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel, StreamFieldPanel, RichTextFieldPanel
from wagtail.api import APIField
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from .blocks import *
from .. import configurations
from ..modules import wagtail_images


class HeroPropertyImage(models.Model):
    intelligence = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    agility = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    strength = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    damage = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    move_speed = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    armor = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        ImageChooserPanel('intelligence'),
        ImageChooserPanel('agility'),
        ImageChooserPanel('strength'),
        ImageChooserPanel('damage'),
        ImageChooserPanel('move_speed'),
        ImageChooserPanel('armor'),
    ]


class HeroesPageMixin:
    @property
    def intelligence_image(self):
        return HeroPropertyImage.objects.first().intelligence

    @property
    def agility_image(self):
        return HeroPropertyImage.objects.first().agility

    @property
    def strength_image(self):
        return HeroPropertyImage.objects.first().strength

    @property
    def damage_image(self):
        return HeroPropertyImage.objects.first().damage

    @property
    def move_speed_image(self):
        return HeroPropertyImage.objects.first().move_speed

    @property
    def armor_image(self):
        return HeroPropertyImage.objects.first().armor


class HeroCategory(models.Model):
    name = models.CharField(max_length=60, null=True, blank=False)

    panels = [
        FieldPanel('name')
    ]

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


@register_snippet
class HeroType(HeroCategory):
    pass


@register_snippet
class HeroAttackType(HeroCategory):
    pass


@register_snippet
class HeroRole(HeroCategory):
    pass


@register_snippet
class Ability(models.Model):
    name = models.TextField(blank=False, unique=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    summary = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=False, null=False
    )
    farsi_summary = RichTextField(
        features=configurations.RICHTEXT_FEATURES, blank=False, null=False
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        RichTextFieldPanel('summary'),
        RichTextFieldPanel('farsi_summary'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Abilities'


@register_snippet
class Hero(models.Model):
    horizontal_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    vertical_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='vertical image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )

    name = models.CharField(max_length=50, blank=False, unique=True)
    farsi_name = models.CharField(max_length=50, blank=False, unique=True)

    popularity = models.IntegerField(default=0)

    ego = models.CharField(
        max_length=10, choices=[
            ('Radiant', 'Radiant'),
            ('Dire', 'Dire'),
        ], blank=False, null=True
    )

    hero_type = models.ForeignKey(
        HeroType, on_delete=models.SET_NULL, null=True, blank=False
    )

    attack_types = models.ManyToManyField(HeroAttackType)

    roles = StreamField(
        [
            ('role', SnippetChooserBlock(HeroRole))
        ], blank=False, null=True
    )

    intelligence = StreamField(
        StreamBlock(
            [
                ('intelligence', Intelligence())
            ], min_num=1, max_num=1, required=True
        ), blank=False, null=True
    )

    agility = StreamField(
        StreamBlock(
            [
                ('agility', Agility())
            ], min_num=1, max_num=1, required=True
        )
    )

    strength = StreamField(
        StreamBlock(
            [
                ('strength', Strength())
            ], min_num=1, max_num=1, required=True
        )
    )

    damage = StreamField(
        StreamBlock(
            [
                ('damage', Damage())
            ], min_num=1, max_num=1, required=True
        )
    )

    move_speed = StreamField(
        StreamBlock(
            [
                ('move_speed', MoveSpeed())
            ], min_num=1, max_num=1, required=True
        )
    )

    armor = StreamField(
        StreamBlock(
            [
                ('armor', Armor())
            ], min_num=1, max_num=1, required=True
        )
    )

    biography = RichTextField(
        null=True, blank=False, features=configurations.RICHTEXT_FEATURES
    )
    farsi_biography = RichTextField(
        null=True, blank=True, features=configurations.RICHTEXT_FEATURES
    )

    hero_abilities = StreamField(
        [
            ('ability', SnippetChooserBlock(Ability))
        ], blank=False, null=True
    )

    farsi_translated = models.BooleanField(default=False)
    english_translated = models.BooleanField(default=False)

    high_quality_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text='high quality image',
        null=True, blank=True, on_delete=models.SET_NULL, related_name='+'
    )
    instagram_ready = models.BooleanField(default=False)

    def get_intelligence(self):
        return self.intelligence[0].value

    def get_agility(self):
        return self.agility[0].value

    def get_strength(self):
        return self.strength[0].value

    def get_damage(self):
        return self.damage[0].value

    def get_move_speed(self):
        return self.move_speed[0].value

    def get_armor(self):
        return self.armor[0].value

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        ImageChooserPanel('horizontal_image'),
                        ImageChooserPanel('vertical_image')
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel('name'), FieldPanel('farsi_name')
                    ]
                ),
                FieldRowPanel(
                    [
                       FieldPanel('popularity')
                    ]
                ),
            ], heading='Details', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                SnippetChooserPanel('hero_type'),
                FieldPanel("attack_types", widget=forms.CheckboxSelectMultiple),
                FieldPanel('ego'),
                StreamFieldPanel('roles'),
            ], heading='categories', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                StreamFieldPanel('intelligence'),
                StreamFieldPanel('agility'),
                StreamFieldPanel('strength'),
                StreamFieldPanel('damage'),
                StreamFieldPanel('move_speed'),
                StreamFieldPanel('armor'),
            ], heading='properties', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('biography'),
                FieldPanel('farsi_biography')
            ], heading='Bio', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                StreamFieldPanel('hero_abilities'),
            ], heading='Abilities', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('farsi_translated'),
                FieldPanel('english_translated')
            ], heading='Translations', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('high_quality_image'),
                FieldPanel('instagram_ready')
            ], heading='Social Media', classname='collapsible collapsed'
        ),
    ]

    @property
    def group(self):
        return self.hero_type.name

    @property
    def hero_attack_types(self):
        return [
            attack_type.name for attack_type in self.attack_types.all()
        ]

    @property
    def hero_roles(self):
        return [
            role.value.name for role in self.roles
        ]

    api_fields = [
        APIField('image', serializer=ImageRenditionField(
            'fill-2000x2000-c80|jpegquality-100', source='high_quality_image')
        ),
        APIField('name'),
        APIField('farsi_name'),
        APIField('ego'),
        APIField('group'),
        APIField('hero_attack_types'),
        APIField('hero_roles'),
        APIField('intelligence'),
        APIField('agility'),
        APIField('strength'),
        APIField('damage'),
        APIField('move_speed'),
        APIField('armor'),
        APIField('biography'),
        APIField('farsi_biography'),
        APIField('hero_abilities'),
        APIField('farsi_translated'),
        APIField('english_translated'),
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        hero_img_title = 'Dota 2 Hero named {}'.format(self.name)
        wagtail_images.set_title(self.horizontal_image, hero_img_title)
        wagtail_images.set_title(self.vertical_image, hero_img_title)
        for ability in self.hero_abilities:
            ability = ability.value
            ability_img_title = "{} ability of {}".format(
                ability.name, self.name
            )
            wagtail_images.set_title(ability.image, ability_img_title)
        super(Hero, self).save()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Heroes'
