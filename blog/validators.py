from django.core import validators


class ImageSize(object):

    def __init__(self, min_w=None, max_w=None, min_h=None, max_h=None):
        self.min_w = min_w
        self.max_w = max_w
        self.min_h = min_h
        self.max_h = max_h

    def __call__(self, im):
        w = im.width
        h = im.height
        tmpl = "The image is {size}; {field} must be {compare} {constraint}px"
        errors = []
        mapping = {"size": "%dX%d" % (w, h)}
        if self.min_w and w < self.min_w:
            mapping["field"] = "width"
            mapping["compare"] = "bigger than"
            mapping["constraint"] = str(self.min_w)
            if self.min_w == self.max_w:
                mapping["compare"] = "exactly"
            errors.append(validators.ValidationError(tmpl.format(**mapping)))
        if self.max_w and w > self.max_w:
            mapping["field"] = "width"
            mapping["compare"] = "smaller than"
            mapping["constraint"] = str(self.max_w)
            if self.min_w == self.max_w:
                mapping["compare"] = "exactly"
            errors.append(validators.ValidationError(tmpl.format(**mapping)))
        if self.min_h and h < self.min_h:
            mapping["field"] = "height"
            mapping["compare"] = "bigger than"
            mapping["constraint"] = str(self.min_h)
            if self.min_h == self.max_h:
                mapping["compare"] = "exactly"
            errors.append(validators.ValidationError(tmpl.format(**mapping)))
        if self.max_h and h > self.max_h:
            mapping["field"] = "height"
            mapping["compare"] = "smaller than"
            mapping["constraint"] = str(self.max_h)
            if self.min_h == self.max_h:
                mapping["compare"] = "exactly"
            errors.append(validators.ValidationError(tmpl.format(**mapping)))
        if errors:
            raise validators.ValidationError(errors)
