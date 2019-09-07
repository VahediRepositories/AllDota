from wagtail.api.v2.endpoints import BaseAPIEndpoint

from .models import Hero


class HeroAPIEndpoint(BaseAPIEndpoint):
    model = Hero
