from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from GAMEDEX.models import Perfil, Producto
 
 
# =====================================
# PRUEBAS UNITARIAS
# =====================================
 
class PruebasUnitarias(TestCase):
 
    def setUp(self):
        """Preparar datos base para todas las pruebas"""
        self.client = Client()
 
        # Crear grupo Cliente
        self.grupo_cliente = Group.objects.create(name="Cliente")
        self.grupo_vendedor = Group.objects.create(name="Vendedor")
 
        # Crear usuario cliente de prueba
        self.usuario = User.objects.create_user(
            username="usuario_test",
            email="test@gamedex.com",
            password="test1234"
        )
        self.usuario.groups.add(self.grupo_cliente)
 
        # Crear usuario vendedor de prueba
        self.vendedor = User.objects.create_user(
            username="vendedor_test",
            email="vendedor@gamedex.com",
            password="test1234"
        )
        self.vendedor.groups.add(self.grupo_vendedor)
 
    def test_usuario_creado_correctamente(self):
        """Verifica que el usuario se crea con los datos correctos"""
        self.assertEqual(self.usuario.username, "usuario_test")
        self.assertEqual(self.usuario.email, "test@gamedex.com")
        self.assertTrue(self.usuario.check_password("test1234"))
 
    def test_perfil_creado_automaticamente(self):
        """Verifica que el signal crea el Perfil automáticamente al crear el usuario"""
        self.assertTrue(hasattr(self.usuario, "perfil"))
        self.assertIsNotNone(self.usuario.perfil)
 
    def test_rol_por_defecto_es_usuario(self):
        """Verifica que el rol por defecto del perfil es Usuario"""
        self.assertEqual(self.usuario.perfil.rol, "Usuario")
 
    def test_password_encriptada(self):
        """Verifica que la contraseña NO se guarda en texto plano"""
        self.assertNotEqual(self.usuario.password, "test1234")
        self.assertTrue(self.usuario.password.startswith("pbkdf2_"))
 
    def test_producto_se_crea_correctamente(self):
        """Verifica que un producto se crea con los datos correctos"""
        producto = Producto.objects.create(
            nombre="Elden Ring",
            descripcion="Videojuego de rol",
            precio=250000,
            cantidad=10,
            dias_garantia=30,
            vendedor=self.vendedor
        )
        self.assertEqual(producto.nombre, "Elden Ring")
        self.assertEqual(producto.precio, 250000)
        self.assertEqual(producto.cantidad, 10)
        self.assertFalse(producto.publicado)
 
    def test_producto_pertenece_al_vendedor(self):
        """Verifica que el producto queda asociado al vendedor correcto"""
        producto = Producto.objects.create(
            nombre="Halo",
            descripcion="Shooter",
            precio=150000,
            cantidad=5,
            dias_garantia=15,
            vendedor=self.vendedor
        )
        self.assertEqual(producto.vendedor.username, "vendedor_test")
 
 
# =====================================
# PRUEBAS DE INTEGRACIÓN
# =====================================
 
class PruebasIntegracion(TestCase):
 
    def setUp(self):
        self.client = Client()
        self.grupo_cliente = Group.objects.create(name="Cliente")
        self.grupo_vendedor = Group.objects.create(name="Vendedor")
        self.grupo_admin = Group.objects.create(name="Administrador")
 
        self.usuario = User.objects.create_user(
            username="cliente_int",
            password="test1234"
        )
        self.usuario.groups.add(self.grupo_cliente)
 
        self.vendedor = User.objects.create_user(
            username="vendedor_int",
            password="test1234"
        )
        self.vendedor.groups.add(self.grupo_vendedor)
 
        self.admin = User.objects.create_user(
            username="admin_int",
            password="test1234"
        )
        self.admin.groups.add(self.grupo_admin)
 
    def test_pagina_login_accesible(self):
        """Integración: la página de login responde correctamente sin autenticación"""
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
 
    def test_pagina_inicio_accesible(self):
        """Integración: la página de inicio es pública y responde"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
 
    def test_registro_publico_accesible(self):
        """Integración: el formulario de registro público responde"""
        response = self.client.get("/registro/")
        self.assertEqual(response.status_code, 200)
 
    def test_login_correcto_redirige_dashboard(self):
        """Integración: login correcto redirige al dashboard"""
        response = self.client.post("/login/", {
            "username": "cliente_int",
            "password": "test1234"
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("/dashboard", response["Location"])
 
    def test_login_incorrecto_no_redirige(self):
        """Integración: credenciales incorrectas no permiten acceso"""
        response = self.client.post("/login/", {
            "username": "cliente_int",
            "password": "claveMAL"
        })
        self.assertEqual(response.status_code, 200)
 
    def test_dashboard_usuario_requiere_login(self):
        """Integración: dashboard de usuario redirige si no está autenticado"""
        response = self.client.get("/dashboard-usuario/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])
 
    def test_dashboard_vendedor_requiere_login(self):
        """Integración: dashboard de vendedor redirige si no está autenticado"""
        response = self.client.get("/dashboard-vendedor/")
        self.assertEqual(response.status_code, 302)
 
    def test_dashboard_admin_requiere_login(self):
        """Integración: dashboard de admin redirige si no está autenticado"""
        response = self.client.get("/dashboard-admin/")
        self.assertEqual(response.status_code, 302)
 
    def test_cliente_accede_su_dashboard(self):
        """Integración: cliente autenticado accede a su dashboard"""
        self.client.login(username="cliente_int", password="test1234")
        response = self.client.get("/dashboard-usuario/")
        self.assertEqual(response.status_code, 200)
 
    def test_vendedor_accede_su_dashboard(self):
        """Integración: vendedor autenticado accede a su dashboard"""
        self.client.login(username="vendedor_int", password="test1234")
        response = self.client.get("/dashboard-vendedor/")
        self.assertEqual(response.status_code, 200)
 
    def test_carrito_requiere_login(self):
        """Integración: el carrito no es accesible sin autenticación"""
        response = self.client.get("/carrito/")
        self.assertEqual(response.status_code, 302)
 
    def test_flujo_completo_registro_y_login(self):
        """Integración: un usuario se registra y luego puede iniciar sesión"""
        # Registro
        response = self.client.post("/registro/", {
            "username": "nuevo_user",
            "email": "nuevo@gamedex.com",
            "password": "nueva1234",
            "rol": "Cliente"
        })
        # Debe redirigir al login después del registro exitoso
        self.assertEqual(response.status_code, 302)
 
        # Login con el nuevo usuario
        login_ok = self.client.login(
            username="nuevo_user",
            password="nueva1234"
        )
        self.assertTrue(login_ok)