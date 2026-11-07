from importlib import import_module
from pathlib import Path

from allauth.utils import build_absolute_uri
from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import RequestFactory, SimpleTestCase
from django.urls import resolve, reverse


class StaticBoundaryTests(SimpleTestCase):
	def test_project_css_is_discoverable(self):
		css_path = finders.find('css/main.css')
		self.assertIsNotNone(css_path)
		self.assertEqual(Path(css_path), settings.BASE_DIR / 'static/css/main.css')
		self.assertIn('background-color', Path(css_path).read_text())

	async def test_django_does_not_serve_static_or_media_files(self):
		self.assertFalse(any('whitenoise' in middleware for middleware in settings.MIDDLEWARE))
		for url in ['/static/css/main.css', '/media/probe.txt']:
			with self.subTest(url=url):
				response = await self.async_client.get(url)
				self.assertEqual(response.status_code, 404)


class BackendRoutingTests(SimpleTestCase):
	def test_backend_pages_and_frontier_routes_are_preserved(self):
		response = self.client.get('/admin/login/')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, '/static/admin/')
		response = self.client.get('/api/schema/swagger-ui/')
		self.assertEqual(response.status_code, 200)
		for name in ['frontier_login', 'frontier_callback']:
			with self.subTest(name=name):
				url = reverse(name)
				self.assertTrue(url.startswith('/users/'))
				self.assertEqual(resolve(url).url_name, name)

	def test_production_settings_recognize_https_and_secure_cookies(self):
		production = import_module('eddai_EliteDangerousApiInterface.settings.prod')
		self.assertTrue(production.CSRF_COOKIE_SECURE)
		self.assertTrue(production.SESSION_COOKIE_SECURE)
		self.assertEqual(production.CSRF_COOKIE_SAMESITE, 'Lax')
		self.assertEqual(production.SESSION_COOKIE_SAMESITE, 'Lax')
		with self.settings(SECURE_PROXY_SSL_HEADER=production.SECURE_PROXY_SSL_HEADER):
			request = RequestFactory().get('/healthz/', HTTP_X_FORWARDED_PROTO='https')
			self.assertTrue(request.is_secure())
			callback = build_absolute_uri(request, reverse('frontier_callback'))
			self.assertTrue(callback.startswith('https://'))
			self.assertFalse(RequestFactory().get('/healthz/').is_secure())

	def test_health_does_not_require_database(self):
		response = self.client.get('/healthz/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'status': 'ok'})

	def test_unknown_routes_use_standard_django_404(self):
		for url in ['/', '/ScrollTextAnimation', '/api/v1/not-a-resource/', '/api/v1/csrf/']:
			with self.subTest(url=url):
				response = self.client.get(url)
				self.assertEqual(response.status_code, 404)
				self.assertTrue(response['Content-Type'].startswith('text/html'))
				self.assertNotIn(b'id="app"', response.content)
