from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('GAMEDEX', '0009_perfil_is_online_perfil_last_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='carrito_guardado',
            field=models.TextField(blank=True, default='{}'),
        ),
    ]
