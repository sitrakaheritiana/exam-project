from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from courses.models import Course
from formations.models import Formation
from students.models import Student
from teachers.models import Teacher


class CourseAccessTests(TestCase):
    def setUp(self):
        self.teacher_user_1 = CustomUser.objects.create_user(
            username="teacher1",
            password="pass1234",
            role="TEACHER",
        )
        self.teacher_user_2 = CustomUser.objects.create_user(
            username="teacher2",
            password="pass1234",
            role="TEACHER",
        )
        self.student_user = CustomUser.objects.create_user(
            username="student1",
            password="pass1234",
            role="STUDENT",
        )

        self.teacher_1 = Teacher.objects.create(
            user=self.teacher_user_1,
            nom="T1",
            prenom="A",
            specialite="Math",
        )
        self.teacher_2 = Teacher.objects.create(
            user=self.teacher_user_2,
            nom="T2",
            prenom="B",
            specialite="Info",
        )

        self.formation_1 = Formation.objects.create(code="F1", libelle="L1")
        self.formation_2 = Formation.objects.create(code="F2", libelle="L2")
        self.formation_1.enseignants.add(self.teacher_1)
        self.formation_2.enseignants.add(self.teacher_2)

        self.student = Student.objects.create(
            user=self.student_user,
            matricule="S-001",
            nom="Student",
            prenom="One",
            formation=self.formation_1,
        )

        self.course_1 = Course.objects.create(
            titre="Algebra",
            fichier_pdf=SimpleUploadedFile("a.pdf", b"%PDF-1.4 course1"),
            formation=self.formation_1,
            enseignant=self.teacher_1,
        )
        self.course_2 = Course.objects.create(
            titre="Networks",
            fichier_pdf=SimpleUploadedFile("b.pdf", b"%PDF-1.4 course2"),
            formation=self.formation_2,
            enseignant=self.teacher_2,
        )

    def test_student_sees_only_own_formation_courses(self):
        self.client.login(username="student1", password="pass1234")
        response = self.client.get(reverse("courses:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra")
        self.assertNotContains(response, "Networks")

    def test_teacher_cannot_edit_other_teacher_course(self):
        self.client.login(username="teacher1", password="pass1234")
        response = self.client.get(reverse("courses:update", args=[self.course_2.pk]))
        self.assertEqual(response.status_code, 404)
