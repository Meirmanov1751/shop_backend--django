from django.utils.safestring import mark_safe


def image_thumbnail(file):
    image_url = file.url
    file_name = str(file)
    return mark_safe(u'<a href="%s" target="_blank"><img src="%s" alt="%s" width="150" height="150"  style="object-fit: ' \
           u'cover;"/></a>' %  (image_url, image_url, file_name))
