# Generated by Django 5.2.1 on 2025-05-31 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_paths', '0003_alter_learningpath_user_alter_learningpath_users'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pathstep',
            unique_together={('learning_path', 'order')},
        ),
    ]
