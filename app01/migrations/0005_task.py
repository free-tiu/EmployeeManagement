# Generated by Django 3.2.4 on 2022-11-14 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('details', models.TextField(verbose_name='详细信息')),
                ('level', models.SmallIntegerField(choices=[(0, '暂定'), (1, '紧急'), (2, '重要'), (3, '临时')], default=0, verbose_name='任务级别')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.admin', verbose_name='任务负责人')),
            ],
        ),
    ]
