from flask.ext.security.forms import LoginForm
from flask.ext.security.utils import get_message

class ExtendedLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(ExtendedLoginForm, self).__init__(*args, **kwargs)
        self.form_errors = []

    def validate(self):
        validation_result = super(ExtendedLoginForm, self).validate()
        self._move_errors()
        return validation_result

    def _move_errors(self):
        self._move_error(self.email, get_message('USER_DOES_NOT_EXIST')[0])
        self._move_error(self.password, get_message('INVALID_PASSWORD')[0])

    def _move_error(self, field, error_message):
        if error_message in field.errors:
            field.errors.remove(error_message)
            self.form_errors.append(error_message)


