

def session_property(key_name, factory=lambda instance: None):
    """
    Turn a variable into a property that is stored in the session with the
    given `key_name.`  Create a default value using `factory` that can utilize
    the instance that owns the property.

    e.x.
        checkout_form = session_property('gifts.order.checkout_form',
            factory=lambda instance: instance._checkout_form_factory())

    Recommended: Use the `session_factory` to decorate a factory method, unless
    the default `factory` is fine for your purposes.
    """

    def _get_from_session(self):
        request = self.request
        value = request.session.get(key_name, __undefined_sentinel)
        if value is __undefined_sentinel:
            return factory(self)
        return value
    _get_from_session.__name__ = '_get_session_%s' % key_name

    def _set_to_session(self, value):
        request = self.request
        session = request.session
        session[key_name] = value
        session.save()
    _set_to_session.__name__ = '_set_session_%s' % key_name

    return property(_get_from_session, _set_to_session)

def session_factory(key_name):
    """ Use this to decorate a factory function for use with `request_variable`

    e.g. turn:
        checkout_form = session_property('gifts.order.checkout_form',
            factory=lambda instance: instance._checkout_form_factory())

    into:

        @session_factory('gifts.order.checkout_form')
        def checkout_form(self):
            return forms.CheckoutForm(self.request.POST or None)

    use like this (real-world example, store the latest valid checkout_from in
    the session):

        def post(self, *args, **kwargs):
            checkout_form = CheckoutForm(request.POST or None)

            if checkout_form.is_valid():
                self.checkout_form = checkout_form

        or

        def get_context_data(self, *args, **kwargs):
            return {
                'checkout_form' : self.checkout_form
            }

    """
    def wrapper(func):
        return session_property(key_name, factory=func)
    return wrapper
