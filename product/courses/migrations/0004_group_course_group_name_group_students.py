# Generated by Django 4.2.10 on 2024-08-19 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_course_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='courses.course', verbose_name='Курс'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='name',
            field=models.CharField(default=1, max_length=100, verbose_name='Название группы'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='student_groups', to=settings.AUTH_USER_MODEL, verbose_name='Студенты'),
        ),
    ]
