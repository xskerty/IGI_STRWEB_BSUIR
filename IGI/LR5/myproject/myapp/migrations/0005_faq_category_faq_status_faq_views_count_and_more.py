# Generated by Django 5.2.2 on 2025-06-05 04:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_faq_options_alter_news_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='category',
            field=models.CharField(choices=[('general', 'Общие вопросы'), ('appointments', 'Запись на прием'), ('services', 'Услуги и цены'), ('doctors', 'Врачи'), ('insurance', 'Страхование'), ('other', 'Другое')], default='general', max_length=20, verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='faq',
            name='status',
            field=models.CharField(choices=[('pending', 'Ожидает ответа'), ('answered', 'Отвечено'), ('closed', 'Закрыто')], default='pending', max_length=20, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='faq',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='Количество просмотров'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=models.TextField(blank=True, null=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='faq',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='faq_questions', to=settings.AUTH_USER_MODEL, verbose_name='Автор вопроса'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.TextField(verbose_name='Вопрос'),
        ),
    ]
