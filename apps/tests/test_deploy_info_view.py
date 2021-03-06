import copy

from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

from apps.views import DeployInfo

from mock import patch, Mock


class InfoViewTest(TestCase):

    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.session = {"tsuru_token": "admin"}
        self.data = {u'Id': u'53e143cb874ccb1f68000001',
                     u'App': u'g1',
                     u'Timestamp': u'18-08-2014 11:29:32',
                     u'Duration': u'00m23s',
                     u'Commit': u'e82nn93nd93mm12o2ueh83dhbd3iu112',
                     u'Error': u'',
                     u'Diff': u'test_diff'}

    @patch("requests.get")
    def test_view(self, get):
        response_mock = Mock()
        response_mock.json.return_value = copy.deepcopy(self.data)
        get.return_value = response_mock
        response = DeployInfo.as_view()(
            self.request,
            deploy="53e143cb874ccb1f68000001",
            app_name="app_name",
        )
        expected = copy.deepcopy(self.data)
        expected["Diff"] = u"""<div class="highlight"><pre>%s\n</pre></div>\n""" % self.data["Diff"]
        self.assertEqual("apps/deploy.html", response.template_name[0])
        self.assertDictEqual(expected, response.context_data['deploy'])
        self.assertIn('app', response.context_data.keys())
        get.assert_called_with(
            '{0}/deploys/{1}'.format(settings.TSURU_HOST,
                                     "53e143cb874ccb1f68000001"),
            headers={'authorization': 'admin'}
        )

    @patch("requests.get")
    def test_view_without_diff(self, get):
        data = copy.deepcopy(self.data)
        del data["Diff"]
        response_mock = Mock()
        response_mock.json.return_value = copy.deepcopy(data)
        get.return_value = response_mock
        response = DeployInfo.as_view()(
            self.request,
            deploy="53e143cb874ccb1f68000001",
            app_name="app_name",
        )
        data["Diff"] = u"""<div class="highlight"><pre>\n</pre></div>\n"""
        self.assertEqual("apps/deploy.html", response.template_name[0])
        self.assertDictEqual(data, response.context_data['deploy'])
        self.assertIn('app', response.context_data.keys())
        get.assert_called_with(
            '{0}/deploys/{1}'.format(settings.TSURU_HOST,
                                     "53e143cb874ccb1f68000001"),
            headers={'authorization': 'admin'}
        )
