from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from . import configuration


class QuotationBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=70)
    farsi_name = blocks.CharBlock(max_length=70, required=False)
    text = blocks.RichTextBlock(features=configuration.RICHTEXT_FEATURES)
    farsi_text = blocks.RichTextBlock(required=False, features=configuration.RICHTEXT_FEATURES)


class IntroductionSection(blocks.StructBlock):
    background = ImageChooserBlock()

    text_place = blocks.ChoiceBlock(
        choices=[
            ('left', 'left'),
            ('right', 'right'),
        ],
    )

    title = blocks.RichTextBlock(features=configuration.RICHTEXT_FEATURES)
    farsi_title = blocks.RichTextBlock(required=False, features=configuration.RICHTEXT_FEATURES)

    description = blocks.RichTextBlock(features=configuration.RICHTEXT_FEATURES)
    farsi_description = blocks.RichTextBlock(required=False, features=configuration.RICHTEXT_FEATURES)

    quotation = QuotationBlock()
