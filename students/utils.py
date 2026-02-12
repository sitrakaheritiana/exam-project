from .models import Student


def get_or_create_student(user):
    student, _ = Student.objects.get_or_create(
        user=user,
        defaults={
            "matricule": f"STD-{user.id}",
            "nom": user.username,
            "prenom": "",
        },
    )
    return student
