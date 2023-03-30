from rest_framework.fields import empty
from rest_framework.serializers import DateTimeField


class FormattedDateTimeField(DateTimeField):
    def __init__(self, format='%H:%M %d-%b-%Y', input_formats=None, default_timezone=None, *args, **kwargs):
        if format is not empty:
            self.format = format
        if input_formats is not None:
            self.input_formats = input_formats
        if default_timezone is not None:
            self.timezone = default_timezone
        super().__init__(*args, **kwargs)
