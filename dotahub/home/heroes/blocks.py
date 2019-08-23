from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from .. import configurations


class PerLevelBlock(blocks.StructBlock):
    base = blocks.IntegerBlock()
    per_level = blocks.FloatBlock()


class Intelligence(PerLevelBlock):
    pass


class Agility(PerLevelBlock):
    pass


class Strength(PerLevelBlock):
    pass


class Damage(blocks.StructBlock):
    min = blocks.IntegerBlock()
    max = blocks.IntegerBlock()


class MoveSpeed(blocks.StructBlock):
    speed = blocks.IntegerBlock()


class Armor(blocks.StructBlock):
    armor = blocks.FloatBlock()


class HeroAbility(blocks.StructBlock):
    name = blocks.CharBlock(max_length=50)
    image = ImageChooserBlock()
    summary = blocks.RichTextBlock(features=configurations.RICHTEXT_FEATURES)
    farsi_summary = blocks.RichTextBlock(required=False, features=configurations.RICHTEXT_FEATURES)
