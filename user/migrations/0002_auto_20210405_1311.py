# Generated by Django 3.1.7 on 2021-04-05 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myusers',
            name='recommended_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='myusers',
            name='referral_code',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]