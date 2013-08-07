import functools
import operator

from django.core.urlresolvers import reverse

from explodio.common import urls


def _clean_short_description(description):
    """
    Clean a system-looking string for display
    :param description: string
    :return: cleaned string
    """
    if isinstance(description, (list, tuple)):
        description = description[0]
    return description.replace('_', ' ')

def prop_formatter(allow_none=False, call_callables=True):
    """
    Format the value of a property for the admin change_list
    :param formatter: Function that takes an instance, attribute's value, and
        optional **kwargs of your choosing, that returns a unicode string with
        or without HTML markup
    :return: A decorated function that can be used in admin.py like this:
        list_display(
            'name',
            'status',
            link('website_url', none='NO LINK', description='URL'),
            object_link('content_page'),
            thumb('image'),
            thumb('thumb', h=120),
            truncate('description', length=30),
        )
    """
    def prop_formatter_decorator(formatter):
        @functools.wraps(formatter)
        def decorator(prop, description=None, none=u'(None)', **format):
            @functools.wraps(formatter)
            def wrapper(obj):
                value = getattr(obj, prop)
                if callable(value) and call_callables:
                    value = value()
                if allow_none or value is not None:
                    return formatter(obj, value, **format)
                else:
                    return none
            wrapper.allow_tags = True
            wrapper.short_description = _clean_short_description(description or prop)
            return wrapper
        return decorator

    return prop_formatter_decorator

def multi_prop_formatter(default_description, call_callables=True):
    """
    Format multiple properties at once, i.e. both Latitude and Longitude
    :param default_description: The default description shown
    :return: A prop_formatter for formatting multiple values at once
    """
    def prop_formatter(formatter):
        @functools.wraps(formatter)
        def decorator(props, description=default_description, **format):
            @functools.wraps(formatter)
            def wrapper(obj):
                values= operator.attrgetter(*props)(obj)
                if call_callables:
                    values = [value() if callable(value) else value
                              for value in values]
                return formatter(obj, values, **format)
            wrapper.allow_tags = True
            wrapper.short_description = _clean_short_description(description)
            return wrapper
        return decorator
    return prop_formatter

def _build_link(obj, url, title, target, title_prop):
    if title_prop:
        title = getattr(obj, title_prop)
    return u'<a href="%(url)s" target="%(target)s">%(title)s</a>' % {
        'url': url,
        'target': target,
        'title' : title,
    }

@prop_formatter()
def link(obj, url, target='_blank', title_prop=None):
    """
    Format a URLField as a link.
    :param obj: instance
    :param url: url value
    :param target: 'a' tag target; "_blank", for example
    :param title_prop: Get the title of the link from this property, otherwise
        just use the URL as the title
    :return: 'a' tag
    """
    return _build_link(obj, url, url, target, title_prop)

@prop_formatter()
def object_link(obj, related, target='_blank', title_prop=None):
    """
    Format a ForeignKey as a link.
    :param obj: instance
    :param related: object to link to using get_absolute_url
    :param target: 'a' tag target; "_blank", for example
    :param title_prop: Get the title of the link from this property, otherwise
        just use the related object the title
    :return: 'a' tag
    """
    url = related.get_absolute_url()
    return _build_link(obj, url, related, target, title_prop)

@prop_formatter()
def edit_object_link(obj, related, target='_self', title_prop=None):
    """
    Format a ForeignKey as a link to admin change_form page.
    :param obj: instance
    :param related: object whose edit page is to be linked to
    :param target: 'a' tag target; "_blank", for example
    :param title_prop: Get the title of the link from this property, otherwise
        just use the related object as the title
    :return: 'a' tag
    """
    url = urls.url_to_edit_object(related)
    return _build_link(obj, url, related, target, title_prop)

@prop_formatter()
def thumb(obj, value, w='', h=80):
    """
    Format an ImageField as an img tag
    :param obj: instance
    :param value: ImageField value
    :param w: Hardcoded image width (not recommended, unless original image
        sizes are static)
    :param h: Hardcoded image height (recommended)
    :return: 'img' tag
    """
    try:
        url = value.url
    except ValueError:
        return u'(None)'
    else:
        return u'<img src="%(url)s" width="%(width)s" height="%(height)s" />' % {
            'url': url,
            'width': w,
            'height': h
        }

@prop_formatter()
def truncate(obj, value, length=80):
    """
    Truncate a CharField's value
    :param obj: instance
    :param value: string to truncate
    :param length: max length of string
    :return: string or string[:max-1] + ...
    """
    value = str(value)
    if len(value) > length:
        return value[:length-1] + u'&hellip;'
    return value

@prop_formatter()
def email(obj, email, target='_blank', title_prop=None):
    """
    Create a 'mailto:' link
    :param obj: instance
    :param email: value
    :param target: 'a' tag target
    :param title_prop: optional link title
    :return: 'a' tag
    """
    return _build_link(obj, 'mailto:%s' % email, email, target, title_prop)

@prop_formatter()
def phone(obj, number, target='_blank', title_prop=None):
    """
    Create a 'tel:' link
    :param obj: instance
    :param number: value
    :param target: 'a' tag target
    :param title_prop: optional link title
    :return: 'a' tag
    """
    return _build_link(obj, 'tel:%s' % number, number, target, title_prop)

@multi_prop_formatter('coordinates')
def lat_long(obj, value, empty='?'):
    """
    Format latitude and longitude like '100S 30W'
    :param obj: instance
    :param value: (latitude, longitude) tuple
    :param empty: When latitude or longitude is None, use this string
    :return: Formatted string
    """
    lat, lng = value

    if lat is not None:
        if lat < 0:
            lat = '%s&deg;S' % abs(lat)
        else:
            lat = '%s&deg;N' % lat
    else:
        lat = '%s&deg;N' % empty

    if lng is not None:
        if lng < 0:
            lng = '%s&deg;W' % abs(lng)
        else:
            lng = '%s&deg;E' % lng
    else:
        lng = '%s&deg;E' % empty

    return '%s %s' % (lat, lng)

@prop_formatter()
def value(obj, value):
    """
    Copy a value to output.
    Can be used for renaming by setting a custom description.
    :param obj: instance
    :param value: value
    :return: value
    """
    return value
