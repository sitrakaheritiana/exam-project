from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from students.models import Student
from teachers.models import Teacher


class RegistrationTests(TestCase):
    def test_register_student_creates_student_profile(self):
        response = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "new_student",
                "email": "s@example.com",
                "role": "STUDENT",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(username="new_student")
        self.assertEqual(user.role, "STUDENT")
        self.assertTrue(Student.objects.filter(user=user).exists())

    def test_register_teacher_creates_teacher_profile(self):
        response = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "new_teacher",
                "email": "t@example.com",
                "role": "TEACHER",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(username="new_teacher")
        self.assertEqual(user.role, "TEACHER")
        self.assertTrue(Teacher.objects.filter(user=user).exists())
