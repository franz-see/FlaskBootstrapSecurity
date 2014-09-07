
from flask_application.ext.flask_security import ExtendedLoginForm
from flask.ext.security.utils import get_message

from tests import UnitTestCase

class TestExtendedLoginForm(UnitTestCase):

    def setUp(self):
        self.extendedLoginForm = ExtendedLoginForm()
        self.extendedLoginForm.csrf_enabled = False

    def test_user_does_not_exist_message(self):
        self.extendedLoginForm.email.data = 'non-existent@user.com'
        self.extendedLoginForm.password.data = 'does not matter'

        self.extendedLoginForm.validate()

        self.log(self.extendedLoginForm)

        assert get_message('USER_DOES_NOT_EXIST')[0] not in self.extendedLoginForm.email.errors
        assert ExtendedLoginForm.MSG_INVALID_USERNAME_OR_PASSWORD in self.extendedLoginForm.form_errors

    def test_invalid_password(self):
        self.extendedLoginForm.email.data = 'matt@lp.com'
        self.extendedLoginForm.password.data = 'incorrect password'

        self.extendedLoginForm.validate()

        self.log(self.extendedLoginForm)

        assert get_message('INVALID_PASSWORD')[0] not in self.extendedLoginForm.password.errors
        assert ExtendedLoginForm.MSG_INVALID_USERNAME_OR_PASSWORD in self.extendedLoginForm.form_errors

    def log(self, form):
        print "form errors : %s" % ', '.join(form.errors)
        print "email errors : %s" % ', '.join(form.email.errors)
        print "password errors : %s" % ', '.join(form.password.errors)



