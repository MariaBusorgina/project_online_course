# Generated by Django 4.2.10 on 2024-08-19 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_group_course_group_name_group_students'),
        ('users', '0002_balance_balance_balance_user_subscription_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_subscriptions', to='courses.group'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_subscriptions', to='courses.course'),
        ),
    ]
