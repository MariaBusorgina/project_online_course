# Generated by Django 4.2.10 on 2024-08-19 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_group_course_group_name_group_students'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('id',), 'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
    ]
