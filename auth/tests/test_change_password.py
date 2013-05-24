from django.test import TestCase
from django.test.client import RequestFactory

from auth.views import ChangePassword


class TestResetPasswordView(TestCase):
    def test_get(self):
        request = RequestFactory().get("/")
        response = ChangePassword.as_view()(request)
        self.assertIn('auth/change_password.html',
                      response.template_name)
