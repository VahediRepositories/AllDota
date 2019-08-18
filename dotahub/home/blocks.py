from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class QuotationBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=70)
    farsi_name = blocks.CharBlock(max_length=70, required=False)
    text = blocks.RichTextBlock()
    farsi_text = blocks.RichTextBlock(required=False)


class IntroductionSection(blocks.StructBlock):
    background = ImageChooserBlock()

    text_place = blocks.ChoiceBlock(
        choices=[
            ('left', 'left'),
            ('right', 'right'),
        ],
    )

    title = blocks.RichTextBlock()
    farsi_title = blocks.RichTextBlock(required=False)

    description = blocks.RichTextBlock()
    farsi_description = blocks.RichTextBlock(required=False)

    quotation = QuotationBlock()
