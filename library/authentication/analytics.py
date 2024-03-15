from django.db.models import Count
from .models import CustomUser


def user_activity_analysis():
    # Кількість користувачів у системі
    total_users = CustomUser.objects.count()

    # Розподіл користувачів за ролями
    role_distribution = CustomUser.objects.values('role').annotate(count=Count('id'))

    return {
        'total_users': total_users,
        'role_distribution': role_distribution
    }

