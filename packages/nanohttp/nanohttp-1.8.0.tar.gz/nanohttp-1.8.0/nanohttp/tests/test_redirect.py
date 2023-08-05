import unittest

from nanohttp import Controller, action, text, HTTPMovedPermanently, HTTPFound
from nanohttp.tests.helpers import WsgiAppTestCase


class HTTPRedirectTestCase(WsgiAppTestCase):

    class Root(Controller):

        @text()
        def index(self):
            raise HTTPMovedPermanently('/new/address')

        @action()
        def about(self):
            raise HTTPFound('/new/address')

    def test_redirect_response_header(self):
        self.assert_get(
            '/',
            status=301,
            expected_headers={'Location': '/new/address'}
        )
        self.assert_get(
            '/about',
            status=302,
            expected_headers={'Location': '/new/address'}
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
