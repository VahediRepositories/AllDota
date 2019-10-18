from rest_framework.fields import Field


class VideoField(Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, video):
        dic = {
            'url': video.url,
            'title': video.title,
            'thumbnail': video.thumbnail
        }
