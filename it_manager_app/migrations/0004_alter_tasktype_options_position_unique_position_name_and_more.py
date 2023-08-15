# Generated by Django 4.2.4 on 2023-08-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_manager_app', '0003_task_unique_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasktype',
            options={'ordering': ['id']},
        ),
        migrations.AddConstraint(
            model_name='position',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_position_name'),
        ),
        migrations.AddConstraint(
            model_name='tasktype',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_type_name'),
        ),
    ]
