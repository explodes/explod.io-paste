

class FormHelpersMixin(object):

    def set_placeholder(self, field, placeholder):
        self.fields[field].widget.attrs['placeholder'] = placeholder

    def set_label(self, field, label):
        self.fields[field].widget.label = label

    def set_default(self, field, value):
        self.fields[field].initial = value

    def set_required(self, field, required=True):
        self.fields[field].required = required

    def set_choices(self, field, choices):
        self.fields[field].choices = choices

    def data_for_key(self, key):
        prefix = '%s-' % self.prefix if self.prefix else ''
        key = '%s%s' % (prefix, key)
        return self.data[key]

    def data_for_key_with_default(self, key, default=None):
        prefix = '%s-' % self.prefix if self.prefix else ''
        key = '%s%s' % (prefix, key)
        return self.data.get(key, default)