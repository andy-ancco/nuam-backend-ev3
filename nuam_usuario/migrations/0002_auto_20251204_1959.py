from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('nuam_usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calificacion',
            name='validado',
            field=models.BooleanField(default=False),
        ),
    ]
