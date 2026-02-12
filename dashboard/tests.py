from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser


class DashboardRoutingTests(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username="admin_dash",
            password="pass1234",
            role="ADMIN",
        )
        self.teacher = CustomUser.objects.create_user(
            username="teacher_dash",
            password="pass1234",
            role="TEACHER",
        )
        self.student = CustomUser.objects.create_user(
            username="student_dash",
            password="pass1234",
            role="STUDENT",
        )

    def test_router_redirects_student(self):
        self.client.login(username="student_dash", password="pass1234")
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertRedirects(response, reverse("dashboard:student"))

    def test_router_redirects_teacher(self):
        self.client.login(username="teacher_dash", password="pass1234")
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertRedirects(response, reverse("dashboard:teacher"))

    def test_router_redirects_admin(self):
        self.client.login(username="admin_dash", password="pass1234")
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertRedirects(response, reverse("dashboard:admin"))


class DebugErrorPagesTests(TestCase):
    def test_debug_403_page(self):
        response = self.client.get(reverse("debug_403"))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")

    def test_debug_404_page(self):
        response = self.client.get(reverse("debug_404"))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
