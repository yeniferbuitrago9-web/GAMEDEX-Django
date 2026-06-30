from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('GAMEDEX', '0010_perfil_carrito_guardado'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.CharField(
                choices=[
                    ('videojuego', 'Videojuego'),
                    ('consola', 'Consola'),
                    ('accesorio', 'Accesorio'),
                    ('periferico', 'Periférico'),
                    ('coleccionable', 'Coleccionable'),
                    ('otro', 'Otro'),
                ],
                default='videojuego',
                max_length=30,
            ),
        ),
    ]
