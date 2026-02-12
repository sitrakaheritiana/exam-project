from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from courses.models import Course
from formations.models import Formation
from grades.models import Grade
from students.models import Student
from teachers.models import Teacher


class GradeRulesTests(TestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            username="admin1",
            password="pass1234",
            role="ADMIN",
        )
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
        self.student_user_1 = CustomUser.objects.create_user(
            username="student1",
            password="pass1234",
            role="STUDENT",
        )
        self.student_user_2 = CustomUser.objects.create_user(
            username="student2",
            password="pass1234",
            role="STUDENT",
        )
        self.student_user_3 = CustomUser.objects.create_user(
            username="student3",
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

        self.formation_1 = Formation.objects.create(code="F1", libelle="Licence 1")
        self.formation_2 = Formation.objects.create(code="F2", libelle="Licence 2")
        self.formation_1.enseignants.add(self.teacher_1)
        self.formation_2.enseignants.add(self.teacher_2)

        self.student_1 = Student.objects.create(
            user=self.student_user_1,
            matricule="S-001",
            nom="Alpha",
            prenom="One",
            formation=self.formation_1,
        )
        self.student_2 = Student.objects.create(
            user=self.student_user_2,
            matricule="S-002",
            nom="Beta",
            prenom="Two",
            formation=self.formation_2,
        )
        self.student_3 = Student.objects.create(
            user=self.student_user_3,
            matricule="S-003",
            nom="Gamma",
            prenom="Three",
            formation=None,
        )

        self.course_1 = Course.objects.create(
            titre="Algebra",
            fichier_pdf=SimpleUploadedFile("a.pdf", b"%PDF-1.4 a"),
            formation=self.formation_1,
            enseignant=self.teacher_1,
        )
        self.course_2 = Course.objects.create(
            titre="Networks",
            fichier_pdf=SimpleUploadedFile("b.pdf", b"%PDF-1.4 b"),
            formation=self.formation_2,
            enseignant=self.teacher_2,
        )

        self.grade_1 = Grade.objects.create(etudiant=self.student_1, course=self.course_1, valeur=15)
        self.grade_2 = Grade.objects.create(etudiant=self.student_2, course=self.course_2, valeur=14)

    def test_teacher_sees_only_his_grades(self):
        self.client.login(username="teacher1", password="pass1234")
        response = self.client.get(reverse("grades:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra")
        self.assertNotContains(response, "Networks")

    def test_admin_sees_all_grades(self):
        self.client.login(username="admin1", password="pass1234")
        response = self.client.get(reverse("grades:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra")
        self.assertContains(response, "Networks")

    def test_teacher_cannot_create_grade_for_other_teacher_course(self):
        self.client.login(username="teacher1", password="pass1234")
        count_before = Grade.objects.count()
        response = self.client.post(
            reverse("grades:create"),
            data={
                "etudiant": self.student_2.pk,
                "course": self.course_2.pk,
                "valeur": 12,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Grade.objects.count(), count_before)

    def test_model_rejects_student_without_formation(self):
        with self.assertRaises(ValidationError):
            Grade.objects.create(etudiant=self.student_3, course=self.course_1, valeur=10)

    def test_student_grade_page_access(self):
        self.client.login(username="student1", password="pass1234")
        response = self.client.get(reverse("grades:student_grades"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra")
