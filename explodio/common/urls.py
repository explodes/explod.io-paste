from django.core.urlresolvers import reverse


def url_to_edit_object(obj):
    name = 'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.module_name)
    url = reverse(name, args=(obj.id,))
    return url
