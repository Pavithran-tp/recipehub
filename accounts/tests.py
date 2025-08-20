from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class PasswordChangeTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'old_secure_password123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        self.password_change_url = reverse('accounts:password_change')
        self.password_change_done_url = reverse('accounts:password_change_done')

    def test_password_change_form_renders_correctly(self):
        response = self.client.get(self.password_change_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_change.html')
        
    def test_successful_password_change(self):
        new_password = 'new_secure_password456'
        response = self.client.post(self.password_change_url, {
            'old_password': self.password,
            'new_password1': new_password,
            'new_password2': new_password
        }, follow=True)
        self.assertRedirects(response, self.password_change_done_url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))
        self.assertFalse(self.user.check_password(self.password))

    def test_unsuccessful_password_change_with_incorrect_old_password(self):
        response = self.client.post(self.password_change_url, {
            'old_password': 'wrong_password',
            'new_password1': 'new_password123',
            'new_password2': 'new_password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('old_password', response.context['form'].errors)
        
    def test_unsuccessful_password_change_with_mismatched_passwords(self):
        response = self.client.post(self.password_change_url, {
            'old_password': self.password,
            'new_password1': 'new_password123',
            'new_password2': 'mismatched_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('new_password2', response.context['form'].errors)
    @override_settings(LOGIN_URL='accounts:login')
    def test_password_change_redirects_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.password_change_url)
        self.assertRedirects(response, reverse('accounts:login') + f'?next={self.password_change_url}')
