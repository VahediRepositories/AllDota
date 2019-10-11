from wagtail.api.v2.endpoints import BaseAPIEndpoint

from .models import SimpleVideo


class SimpleVideoAPIEndpoint(BaseAPIEndpoint):
    model = SimpleVideo
