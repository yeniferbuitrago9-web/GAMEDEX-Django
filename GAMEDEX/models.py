from django.db import models
from django.contrib.auth.models import User


# =========================
# PERFIL DE USUARIO
# =========================
class Perfil(models.Model):

    ROLES = (
        ('Usuario', 'Usuario'),
        ('Vendedor', 'Vendedor'),
        ('Administrador', 'Administrador'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='Usuario'
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    direccion = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True, blank=True)
    carrito_guardado = models.TextField(default="{}", blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
    



# =========================
# PRODUCTO
# =========================
class Producto(models.Model):

    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    cantidad = models.PositiveIntegerField(default=1)
    dias_garantia = models.PositiveIntegerField(default=0)

    imagen = models.ImageField(
        upload_to="productos/",
        null=True,
        blank=True,
        default="productos/default.png"  # 👈 evita errores si no hay imagen
    )

    publicado = models.BooleanField(default=False)
    destacado = models.BooleanField(default=False)  # 👈 clave para productos destacados

    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
# =========================
# comunidades 
# =========================

class Comunidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='comunidades/', null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.nombre


class Publicacion(models.Model):
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='posts/', null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)


    # 👍 Likes reales
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def total_likes(self):
        return self.likes.count()


class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    
