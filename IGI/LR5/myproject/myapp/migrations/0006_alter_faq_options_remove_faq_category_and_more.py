# Generated by Django 5.2.2 on 2025-06-05 05:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_faq_category_faq_status_faq_views_count_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['-created_at'], 'verbose_name': 'Вопрос-ответ', 'verbose_name_plural': 'Вопросы-ответы'},
        ),
        migrations.RemoveField(
            model_name='faq',
            name='category',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='status',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='views_count',
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answered_faqs', to=settings.AUTH_USER_MODEL, verbose_name='Автор ответа'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
