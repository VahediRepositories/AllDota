from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from .. import configurations


class QuotationBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=70)
    farsi_name = blocks.CharBlock(max_length=70, required=False)
    text = blocks.RichTextBlock(features=configurations.RICHTEXT_FEATURES)
    farsi_text = blocks.RichTextBlock(required=False, features=configurations.RICHTEXT_FEATURES)


class IntroductionSection(blocks.StructBlock):
    background = ImageChooserBlock()

    text_place = blocks.ChoiceBlock(
        choices=[
            ('left', 'left'),
            ('right', 'right'),
        ],
    )

    title = blocks.RichTextBlock(features=configurations.RICHTEXT_FEATURES)
    farsi_title = blocks.RichTextBlock(required=False, features=configurations.RICHTEXT_FEATURES)

    description = blocks.RichTextBlock(features=configurations.RICHTEXT_FEATURES)
    farsi_description = blocks.RichTextBlock(required=False, features=configurations.RICHTEXT_FEATURES)

    quotation = QuotationBlock()
