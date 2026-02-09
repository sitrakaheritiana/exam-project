from .models import Teacher

def get_or_create_teacher(user):
    teacher, _ = Teacher.objects.get_or_create(
        user=user,
        defaults={
            'nom': user.username,
            'specialite': 'Non définie'
        }
    )
    return teacher
