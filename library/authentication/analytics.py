# analytics.py
from django.db.models import Count
from .models import CustomUser


def user_activity_analysis():
    # Количество пользователей в системе
    total_users = CustomUser.objects.count()

    # Распределение пользователей по ролям
    role_distribution = CustomUser.objects.values('role').annotate(count=Count('id'))

    return {
        'total_users': total_users,
        'role_distribution': role_distribution
    }


# def session_analysis():
#     # Общее количество активных сессий в системе
#     active_sessions_count = DjangoSession.objects.count()
#
#     return {
#         'active_sessions_count': active_sessions_count
#     }
