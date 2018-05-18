"""Tests exception handling in :mod:`arxiv.base.exceptions`."""

from unittest import TestCase, mock
from flask import Flask

from arxiv import status
from browse.factory import create_web_app
from browse.services.document.metadata import AbsException
from werkzeug.exceptions import InternalServerError


class TestExceptionHandling(TestCase):
    """HTTPExceptions should be handled with custom templates."""

    def setUp(self):
        """Initialize an app and install :class:`.Base`."""
        self.app = create_web_app()
        self.client = self.app.test_client()

    def test_404(self):
        """A 404 response should be returned."""
        for path in ('/foo', '/abs', '/abs/'):
            response = self.client.get(path)
            self.assertEqual(response.status_code,
                             status.HTTP_404_NOT_FOUND,
                             f'should get 404 for {path}')
            self.assertIn('text/html', response.content_type)

    @mock.patch('browse.controllers.abs.get_abs_page')
    def test_500(self, mock_abs):
        """A 500 response should be returned."""
        # Raise a general exception from the get_abs_page controller.
        mock_abs.side_effect = AbsException

        response = self.client.get('/abs/1234.5678')
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('text/html', response.content_type)