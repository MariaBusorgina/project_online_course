from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer, CourseBaseSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription, Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        if self.request.user.is_staff:
            return course.lessons.all()

        if not Subscription.objects.filter(user=self.request.user, course=course).exists():
            raise PermissionDenied("Вы не подписаны на этот курс")

        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.prefetch_related('students').order_by('-id')


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_queryset(self):
        if self.get_serializer_class() == CourseSerializer:
            return self.get_all_courses_queryset()
        return self.get_available_courses_queryset()

    def get_all_courses_queryset(self):
        """Возвращает все курсы."""
        return Course.objects.all().prefetch_related('lessons', 'groups__students', 'course_subscriptions')

    def get_available_courses_queryset(self):
        """Возвращает доступные для покупки курсы для пользователя."""
        user = self.request.user
        return Course.objects.filter(is_available=True) \
            .exclude(course_subscriptions__user=user) \
            .prefetch_related('lessons')

    def get_serializer_class(self):
        if 'available-courses' in self.request.path:
            return CourseBaseSerializer
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        # TODO
        course = get_object_or_404(Course, pk=pk)
        user = request.user

        if not course.is_available:
            return Response(
                {"detail": "Курс недоступен для покупки."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Subscription.objects.filter(user=user, course=course).exists():
            return Response(
                {"detail": "Вы уже подписаны на этот курс."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_balance = get_object_or_404(Balance, user=user)
        if user_balance.balance < course.price:
            return Response(
                {"detail": "Недостаточно бонусов для покупки курса"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Списание бонусов и создание подписки
        user_balance.balance -= course.price
        user_balance.save()

        subscription = Subscription.objects.create(user=user, course=course)
        data = {
            "detail": "Подписка на курс успешно оформлена.",
            "course": {
                "id": course.id,
                "title": course.title,
                "price": course.price,
            },
            "subscription": {
                "id": subscription.id,
                "user": user.id,
                "created_at": subscription.date_subscribed,
            },
            "user": {
                "balance": user_balance.balance
            }
        }

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )
