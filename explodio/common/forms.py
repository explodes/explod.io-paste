

class FormHelpersMixin(object):
    """
    Quick and easy functions for common form __init__ tasks
    """

    def set_placeholder(self, field, placeholder):
        """
        Set place holder text for a field
        :param field: Field name
        :param placeholder: Placeholder text
        """
        self.fields[field].widget.attrs['placeholder'] = placeholder

    def set_label(self, field, label):
        """
        Set label for a field
        :param field: Field name
        :param label: Label text
        """
        self.fields[field].widget.label = label

    def set_default(self, field, value):
        """
        Set default for a field
        :param field: Field name
        :param value: Default value
        """
        self.fields[field].initial = value

    def set_required(self, field, required=True):
        """
        Set a field's requiredness
        :param field: Field name
        :param required: Whether or not it is required
        """
        self.fields[field].required = required

    def set_choices(self, field, choices):
        """
        Set a field's choices
        :param field: Field name
        :param choices: (value, name) tuple of choices
        """
        self.fields[field].choices = choices

    def data_for_key(self, key):
        """
        Get a value from self.data taking self.prefix into account
        :param key: Key name
        :return: Value of self.data[key]
        """
        prefix = '%s-' % self.prefix if self.prefix else ''
        key = '%s%s' % (prefix, key)
        return self.data[key]

    def data_for_key_with_default(self, key, default=None):
        """
        Get a value from self.data taking self.prefix into account, returning a
        default value if the key is not present
        :param key: Key name
        :param default: Value to return when key is not present in self.data
        :return: Value of self.data[key] or default
        """
        prefix = '%s-' % self.prefix if self.prefix else ''
        key = '%s%s' % (prefix, key)
        return self.data.get(key, default)
