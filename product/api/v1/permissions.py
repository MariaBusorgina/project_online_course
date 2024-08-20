from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


def make_payment(request):
    # TODO
    pass


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        # TODO
        if request.user and request.user.is_staff:
            return True

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Разрешение на создание/обновление/удаление для всех пользователей, которые уже имеют доступ
        return False

    def has_object_permission(self, request, view, obj):
        # TODO
        if request.user and request.user.is_staff:
            return True

        if obj is not None and hasattr(obj, 'course'):
            # Проверяем, есть ли у пользователя подписка на курс
            return Subscription.objects.filter(user=request.user, course=obj.course).exists()

        return False


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
