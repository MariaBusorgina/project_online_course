from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers

from courses.models import Course, Group, Lesson
from users.models import Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    # TODO Доп. задание
    course = serializers.StringRelatedField(read_only=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = (
            'name',
            'course',
            'students',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CourseBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для списка доступных курсов."""

    lessons_count = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
        )


class CourseSerializer(CourseBaseSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        # TODO Доп. задание
        return obj.groups.aggregate(total_students=Count('students'))['total_students']

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел."""
        # TODO Доп. задание
        # Считаем количество студентов для каждой группы
        groups = obj.groups.annotate(num_students=Count('students'))

        if not groups:
            return 0

        # Среднее количество студентов в группах
        avg_students = groups.aggregate(average_students=Avg('num_students'))['average_students']

        # Максимальное количество студентов в группе
        max_students_per_group = 30

        filled_percent = (avg_students / max_students_per_group) * 100

        return round(filled_percent, 2)

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        # TODO Доп. задание
        # Количество подписок на курс
        subscriptions_count = obj.course_subscriptions.count()

        # Общее количество пользователей на платформе
        total_users_count = User.objects.count()

        # Если нет пользователей
        if total_users_count == 0:
            return 0

        demand_percent = (subscriptions_count / total_users_count) * 100

        return round(demand_percent, 2)

    class Meta(CourseBaseSerializer.Meta):
        fields = CourseBaseSerializer.Meta.fields + (
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = (
            'title',
            'author',
            'start_date',
            'price',
            'is_available'
        )
