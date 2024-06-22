# Generated by Django 5.0.6 on 2024-06-02 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0006_founder_picture'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProjectImage',
            new_name='Image',
        ),
        migrations.AddField(
            model_name='category',
            name='picture',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to='main_app.image',
            ),
        ),
        migrations.AddField(
            model_name='news',
            name='picture',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to='main_app.image',
            ),
        ),
    ]