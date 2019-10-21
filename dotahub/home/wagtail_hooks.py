import os

from django.core.files import File
from moviepy.video.io.VideoFileClip import VideoFileClip
from wagtail.core import hooks
from .models import *


@hooks.register('after_create_page')
def after_create_short_video_page(request, page):
    print('@@@@@@@@@@@@@@@@@@@@@@@@  creating')
    page = page.specific
    if isinstance(page, ShortVideoPage):
        set_short_video_page_thumbnail(page)


@hooks.register('after_edit_page')
def after_edit_short_video_page(request, page):
    print('@@@@@@@@@@@@@@@@@@@@@@@  editing')
    page = page.specific
    if isinstance(page, ShortVideoPage):
        set_short_video_page_thumbnail(page)


def set_short_video_page_thumbnail(page):
    generated_file = False
    if page.video.thumbnail:
        file = open(page.video.thumbnail.path, 'rb')
        file = File(file)
    else:
        clip = VideoFileClip(page.video.file.path)
        generated_file = 'thumbnail.jpeg'
        clip.save_frame(generated_file, t=0)
        file = open(generated_file, 'rb')
        file = File(file)
    thumbnail = Image(
        title=text_processing.html_to_str(
            page.english_title
        ), file=file
    )
    thumbnail.save()
    page.thumbnail = thumbnail
    page.save()
    if generated_file:
        os.remove(generated_file)
