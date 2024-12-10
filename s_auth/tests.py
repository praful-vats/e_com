from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden


class AuthenticationTests(TestCase):
    def setUp(self):
        """Create a user for testing purposes."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_register_view_get(self):
        """Test if the registration page renders correctly."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_valid(self):
        """Test if the registration form works correctly."""
        response = self.client.post(reverse('register'), data={
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        """Test if the registration form gives errors when data is invalid."""
        response = self.client.post(reverse('register'), data={
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'wrongpassword',
        })
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

    def test_login_view_get(self):
        """Test if the login page renders correctly."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        """Test if the login form works with valid credentials."""
        response = self.client.post(reverse('login'), data={
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_view_post_invalid(self):
        """Test if the login form shows error with invalid credentials."""
        response = self.client.post(reverse('login'), data={
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertContains(response, 'Invalid credentials')

    def test_logout_view(self):
        """Test if the logout view logs out the user and redirects to login."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_dashboard_view_authenticated(self):
        """Test if authenticated users can access the dashboard."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_view_unauthenticated(self):
        """Test if unauthenticated users are redirected to login."""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('login') + '?next=/dashboard/')

    def test_admin_panel_view_authenticated_staff(self):
        """Test if authenticated staff users can access the admin panel."""
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel.html')

    def test_admin_panel_view_authenticated_non_staff(self):
        """Test if authenticated non-staff users are forbidden from accessing admin panel."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('admin_panel'))
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "You do not have permission to access this page.")

    def test_admin_panel_view_unauthenticated(self):
        """Test if unauthenticated users are redirected to login for admin panel."""
        response = self.client.get(reverse('admin_panel'))
        self.assertRedirects(response, reverse('login') + '?next=/admin-panel/')


# Custom Login Form Tests (if any customization in forms is present)
class CustomLoginFormTests(TestCase):
    def test_custom_login_form_invalid(self):
        """Test if the custom login form returns an error for invalid credentials."""
        response = self.client.post(reverse('login'), data={
            'username': 'invaliduser',
            'password': 'invalidpassword',
        })
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_custom_login_form_valid(self):
        """Test if the custom login form works with valid credentials."""
        self.client.post(reverse('register'), data={
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        response = self.client.post(reverse('login'), data={
            'username': 'newuser',
            'password': 'newpassword123',
        })
        self.assertRedirects(response, reverse('dashboard'))
