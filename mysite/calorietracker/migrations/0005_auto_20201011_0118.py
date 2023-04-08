# Generated by Django 3.1.2 on 2020-10-11 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calorietracker', '0004_auto_20201010_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='activity',
            field=models.CharField(blank=True, choices=[('1', 'Sedentary (little or no exercise)'), ('2', 'Lightly active (light exercise/sports 1-3 days/week)'), ('3', 'Moderatetely active (moderate exercise/sports 3-5 days/week)'), ('4', 'Very active (hard exercise/sports 6-7 days a week)'), ('5', 'Extra active (very hard exercise/sports & physical job or 2x training)')], default='1', help_text='Used to estimate your total daily energy expenditure until we have enough data to calculate it', max_length=1, null=True),
        ),
    ]
