from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адреса /about/author/."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адреса /about/tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса /page/tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertTemplateUsed(response, 'app_name/tech.html')

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса /page/author/."""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response, 'app_name/author.html')
