# Generated by Django 4.2.1 on 2023-06-10 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0002_remove_friend_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incomingfriendrequest',
            old_name='from_user',
            new_name='from_whom',
        ),
        migrations.RenameField(
            model_name='incomingfriendrequest',
            old_name='to_user',
            new_name='to_whom',
        ),
        migrations.RenameField(
            model_name='outgoingfriendrequest',
            old_name='from_user',
            new_name='from_whom',
        ),
        migrations.RenameField(
            model_name='outgoingfriendrequest',
            old_name='to_user',
            new_name='to_whom',
        ),
    ]