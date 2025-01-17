# Generated by Django 4.2.10 on 2024-08-19 04:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_is_available_lesson_course'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=1000.0, max_digits=10, verbose_name='Баланс'),
        ),
        migrations.AddField(
            model_name='balance',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='courses.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='date_subscribed',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
