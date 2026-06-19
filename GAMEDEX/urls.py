from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect, render

def inicio(request):
    return render(request, 'inicio.html')


urlpatterns = [

     path('', inicio),  
    path('inicio/', inicio, name='inicio'),
    path('api/productos/', views.api_productos, name='api_productos'),

    path('admin/', admin.site.urls),
    
    #inventario admin
    path("inventario-admin/", views.inventario_admin, name="inventario_admin"),
    path("eliminar-producto/<int:id>/", views.eliminar_producto_admin, name="eliminar_producto_admin"),


    # Login y Logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),

    # Redirección inteligente después del login
    path('dashboard/', views.redireccion_dashboard, name='dashboard'),

    # Dashboards por rol
    path('dashboard-usuario/', views.dashboard_usuario, name='dashboard_usuario'),
    path('dashboard-vendedor/', views.dashboard_vendedor, name='dashboard_vendedor'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),

    # Administración de usuarios
    path('editar-usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('registro/', views.registro_publico, name='registro_publico'),

    # Panel vendedor
    path('crear-producto/', views.crear_producto, name='crear_producto'),
    path("editar-producto/<int:producto_id>/", views.editar_producto, name="editar_producto"),
    path('publicar/<int:producto_id>/', views.toggle_publicacion, name='toggle_publicacion'),


    #agregar al carrito
    path("agregar_carrito/<int:producto_id>/", views.agregar_carrito, name="agregar_carrito"),

    #quitar productos del carrito del usuario
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("quitar_unidad/<int:producto_id>/", views.quitar_unidad, name="quitar_unidad"),
    path("eliminar_producto/<int:producto_id>/", views.eliminar_producto, name="eliminar_producto"),

    #comprar carrito
    path("comprar/", views.comprar_carrito, name="comprar_carrito"),
    path("factura/", views.factura, name="factura"),
    path("descargar-factura/", views.descargar_factura_pdf, name="descargar_factura_pdf"),

    #editar perfil
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),


    path("exportar-pdf/", views.exportar_pdf_vendedor, name="exportar_pdf_vendedor"),
    path("exportar-excel/", views.exportar_excel_vendedor, name="exportar_excel_vendedor"),


    path('exportar-pdf-usuarios/', views.exportar_pdf_usuarios, name='exportar_pdf_usuarios'),
    path('exportar-excel-usuarios/', views.exportar_excel_usuarios, name='exportar_excel_usuarios'),

    path('inventario/pdf/', views.exportar_pdf_inventario, name='exportar_pdf_inventario'),
    path('inventario/excel/', views.exportar_excel_inventario, name='exportar_excel_inventario'),


    path('destacar/<int:producto_id>/', views.toggle_destacado, name='toggle_destacado'),


    path('comunidades/', views.lista_comunidades, name='comunidades'),
    path('comunidad/<int:id>/', views.ver_comunidad, name='ver_comunidad'),
    path('comunidad/crear/', views.crear_comunidad, name='crear_comunidad'),
    path('comunidad/<int:id>/editar/', views.editar_comunidad, name='editar_comunidad'),
    path('comunidad/<int:id>/eliminar/', views.eliminar_comunidad, name='eliminar_comunidad'),

    path('like/<int:id>/', views.dar_like, name='dar_like'),
    path('comentar/<int:id>/', views.comentar, name='comentar'),
        
    path('comunidad/<int:id>/crear_publicacion/', views.crear_publicacion_ajax, name='crear_publicacion_ajax'),
     path('eliminar_publicacion/<int:post_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
]

#  SOLUCIÓN DEFINITIVA PARA IMÁGENES EN RENDER (FUNCIONA CON DEBUG=FALSE)
if settings.MEDIA_URL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)