from django.urls import path
from django.contrib.auth.views import LogoutView
from polls import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("defemociones", views.defemociones, name="defemociones"),
    path("perfil/<str:username>/", views.perfil, name="perfil"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.inicioSesion, name="login"),
    path("logout/", views.cerrarSesion, name="logout"),
    path("nuevaObra", views.nuevaObra, name="nuevaObra"),
    path("mis_obras", views.mis_obras, name="mis_obras"),
    path('editar_perfil/<str:username>/', views.editar_perfil, name='editar_perfil'),
    path("editar_capitulo/<int:capitulo_id>/", views.editar_capitulo, name="editar_capitulo"),
    path("capitulos_obra/<int:obra_id>/", views.capitulos_obra, name="capitulos_obra"),
    path('editar_obra/<int:obra_id>/', views.editar_obra, name='editar_obra'),
    path('eliminar_obra/<int:obra_id>/', views.eliminar_obra, name='eliminar_obra'),
    path('eliminar_capitulo/<int:capitulo_id>/', views.eliminar_capitulo, name='eliminar_capitulo'),
    path("nuevoCapitulo/<int:obra_id>/", views.nuevoCapitulo, name="nuevoCapitulo"),
    path("catalogo", views.catalogo, name="catalogo"),
    path('obra/<int:obra_id>/<int:capitulo_id>/', views.detalle_obra, name='detalle_obra'),
    path('comentario/edit/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('comentario/delete/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('buscar_obras/', views.buscar_obras, name='buscar_obras'),
    path('like_capitulo/<int:obra_id>/<int:capitulo_id>/', views.like_capitulo, name='like_capitulo'),
    path('perfil/favoritos/<str:username>/', views.favoritos, name='favoritos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)