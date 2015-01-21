from PIL import Image
from StringIO import StringIO

from django.core import validators


class ImageWidth(object):

    def __init__(self, width, height,
                 error_message="The image isn'tas large as expected!"):
        self.w, self.h, self.error_message = width, height, error_message

    def __call__(self, field_data, all_data):
        im = Image.open(StringIO(field_data['content']))
        if im.size[0] != self.w or im.size[1] != self.h:
            raise validators.ValidationError, self.error_message
