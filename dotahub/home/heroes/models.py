from django import forms
from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel, StreamFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from ..modules import wagtail_images
from .blocks import *
from .. import configurations


class HeroPropertyImage(models.Model):
    intelligence = models.ForeignKey(
        'wagtailimages.Image',
        help_text='horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    agility = models.ForeignKey(
        'wagtailimages.Image',
        help_text='horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    strength = models.ForeignKey(
        'wagtailimages.Image',
        help_text='horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    damage = models.ForeignKey(
        'wagtailimages.Image',
        help_text='horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    move_speed = models.ForeignKey(
        'wagtailimages.Image',
        help_text='horizontal image',
        null=True, blank=False, on_delete=models.SET_NULL, related_name='+'
    )
    armor = models.ForeignKey(
        'wagtailimages.Image',
        help_text='horizontal image',
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
        return HeroPropertyImage.objects.all()[0].intelligence

    @property
    def agility_image(self):
        return HeroPropertyImage.objects.all()[0].agility

    @property
    def strength_image(self):
        return HeroPropertyImage.objects.all()[0].strength

    @property
    def damage_image(self):
        return HeroPropertyImage.objects.all()[0].damage

    @property
    def move_speed_image(self):
        return HeroPropertyImage.objects.all()[0].move_speed

    @property
    def armor_image(self):
        return HeroPropertyImage.objects.all()[0].armor


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

    ego = models.CharField(
        max_length=10, choices=[
            ('Radiant', 'Radiant'),
            ('Dire', 'Dire'),
        ], blank=False, null=True
    )

    type = models.ForeignKey(
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

    abilities = StreamField(
        [
            ('ability', HeroAbility())
        ], null=True, blank=True
    )

    farsi_translated = models.BooleanField(default=False)

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
            ], heading='Details', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                SnippetChooserPanel('type'),
                FieldRowPanel(
                    [
                        FieldPanel("attack_types", widget=forms.CheckboxSelectMultiple),
                        FieldPanel('ego'),
                    ]
                ),
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
                StreamFieldPanel('abilities')
            ], heading='Abilities', classname='collapsible collapsed'
        ),
        MultiFieldPanel(
            [
                FieldPanel('farsi_translated')
            ], heading='Translations', classname='collapsible collapsed'
        )
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name:
            hero_img_title = 'Dota 2 Hero named {}'.format(self.name)
            wagtail_images.set_title(self.horizontal_image, hero_img_title)
            wagtail_images.set_title(self.vertical_image, hero_img_title)
            for ability in self.abilities:
                ability = ability.value
                if ability['name']:
                    ability_img_title = "{} ability of {}".format(
                        ability['name'], self.name
                    )
                    wagtail_images.set_title(ability['image'], ability_img_title)
        super(Hero, self).save()

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Heroes'
