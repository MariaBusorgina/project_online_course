from django.conf import settings
from django.db import transaction
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from courses.models import Group
from users.models import Subscription, Balance


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """Распределение нового студента в группу курса."""
    if created:
        # TODO
        course = instance.course
        user = instance.user

        groups = Group.objects.filter(course=course)
        if not groups.exists():
            for i in range(1, 11):
                Group.objects.create(name=f'Группа {i}', course=course)

        groups = list(Group.objects.filter(course=course))
        group_count = len(groups)

        # Распределение пользователей по группам
        with transaction.atomic():
            # Определение всех подписчиков на курс
            subscriptions = Subscription.objects.filter(course=course)
            new_user_index = subscriptions.count() - 1

            group = groups[new_user_index % group_count]
            instance.group = group
            instance.save()

            group.students.add(user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_balance(sender, instance, created, **kwargs):
    """Создание объекта Balance при создании нового пользователя."""
    if created:
        Balance.objects.create(user=instance)