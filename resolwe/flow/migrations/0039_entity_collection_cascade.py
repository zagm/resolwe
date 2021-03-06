# Generated by Django 2.2.2 on 2019-07-24 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0038_remove_m2m_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data', to='flow.Collection'),
        ),
        migrations.AlterField(
            model_name='data',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data', to='flow.Entity'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flow.Collection'),
        ),
    ]
