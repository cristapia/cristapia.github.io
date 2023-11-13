from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .models import Obra
from django.db.models import Q, Sum, Count

def index(request):
    obras = Obra.objects.all()

    first_chapters = {}

    for obra in obras:
        first_chapter = obra.capitulos.all()
        first_chapters[obra.id] = first_chapter
    return render(request, "index.html", {'obras': obras, 'first_chapters': first_chapters})

def defemociones(request):
    return render(request, "defemociones.html", {})

def catalogo(request):
    obras = Obra.objects.all().order_by('id')

    first_chapters = {}

    for obra in obras:
        first_chapter = obra.capitulos.all()
        first_chapters[obra.id] = first_chapter

        obra.total_likes = obra.get_total_likes_all_capitulos()

    return render(request, "catalogo.html", {'obras': obras, 'first_chapters': first_chapters})

@login_required(login_url='index')
def perfil(request, username):
    user_obras = Obra.objects.filter(usuario__username=username).order_by('id')
    usuario = get_object_or_404(Usuario, username=username)
    first_chapters = {}
    total_user_likes = usuario.get_all_likes().count()

    for obra in user_obras:
        first_chapter = obra.capitulos.all()
        first_chapters[obra.id] = first_chapter

    return render(request, 'perfil.html', {'user_obras': user_obras, 'usuario': usuario, 'first_chapters': first_chapters, 'total_user_likes': total_user_likes})

def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Cuenta creada para ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/registro.html', context)

def inicioSesion(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Usuario o Contraseña incorrectos.')

        context = {}
        return render(request, 'accounts/login.html', context)
    
def cerrarSesion(request):
    logout(request)
    return redirect('index')

@login_required(login_url='index')
def nuevaObra(request):
    if request.method == 'POST':
        form = CrearObra(request.POST, request.FILES)
        form.instance.usuario = request.user
        if form.is_valid():
            form.save()
            return redirect('nuevoCapitulo', obra_id=form.instance.id)
    else:
        form = CrearObra(initial={'usuario': request.user})

    return render(request, 'obra/nuevaObra.html', {'form': form})

@login_required(login_url='index')
def nuevoCapitulo(request, obra_id):
    obra = Obra.objects.get(pk=obra_id)

    if request.method == 'POST':
        form = CapituloForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.obra = obra
            chapter.save()
            return redirect('capitulos_obra', obra_id=obra_id)
    else:
        form = CapituloForm()

    return render(request, 'obra/nuevoCapitulo.html', {'obra': obra, 'obra_id': obra_id, 'form': form})

def detalle_obra(request, obra_id, capitulo_id):
    obra = get_object_or_404(Obra, pk=obra_id)
    capitulos = obra.capitulos.all().order_by('orden')
    capitulo = get_object_or_404(Capitulos, id=capitulo_id, obra=obra)
    comentarios = Comentarios.objects.filter(capitulo=capitulo)
    next_chapter = Capitulos.objects.filter(obra=obra, id__gt=capitulo_id).order_by('id').first()

    user_likes_capitulo = False
    if request.user.is_authenticated:
        user_likes_capitulo = capitulo.capitulo_likes.filter(user=request.user).exists()

    info_autor = {
    'foto_perfil': obra.usuario.foto_perfil,
    'username': obra.usuario.username,
    'social_media': {
        'twitter': obra.usuario.twitter,
        'facebook': obra.usuario.facebook,
        'instagram': obra.usuario.instagram,
        'tumblr': obra.usuario.tumblr,
    },
    }
    if request.method == 'POST':
        form = FormularioComentario(request.POST)
        if form.is_valid():
            comentarios = form.save(commit=False)
            comentarios.usuario = request.user
            comentarios.capitulo = capitulo
            comentarios.save()
            return redirect('detalle_obra', obra_id=obra_id, capitulo_id=capitulo_id)
    else:
        form = FormularioComentario()
    return render(request, 'catalogo/detalle_obra.html', {'obra': obra, 'comentarios': comentarios, 'capitulos': capitulos, 'form': form, 'usuario': request.user, 'info_autor': info_autor, 'capitulo': capitulo, 'next_chapter': next_chapter, 'user_likes_capitulo': user_likes_capitulo})

@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentarios, pk=comentario_id)
    capitulo = comentario.capitulo
    if request.user == comentario.usuario:
        if request.method == 'POST':
            form = FormularioComentario(request.POST, instance=comentario)
            if form.is_valid():
                form.save()
                return redirect('detalle_obra', obra_id=capitulo.obra.id, capitulo_id=capitulo.id)
        else:
            form = FormularioComentario(instance=comentario)
        return render(request, 'catalogo/editar_comentario.html', {'form': form, 'comentario': comentario})
    else:
        pass

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentarios, pk=comentario_id)
    capitulo = comentario.capitulo
    
    if request.user == comentario.usuario or request.user.has_perm('polls.eliminar_comentario'):
        if request.method == 'POST':
            comentario.delete()
            return redirect('detalle_obra', obra_id=capitulo.obra.id, capitulo_id=capitulo.id)
        return render(request, 'catalogo/eliminar_comentario.html', {'comentario': comentario})
    else:
        pass

@login_required
def mis_obras(request):
    obras_usuario = Obra.objects.filter(usuario=request.user).order_by('id')
    return render(request, "perfil/mis_obras.html", {'obras_usuario': obras_usuario})

@login_required
def editar_obra(request, obra_id):
    obra = get_object_or_404(Obra, pk=obra_id)
    if request.method == 'POST':
        form = CrearObra(request.POST, instance=obra)
        if form.is_valid():
            form.save()
            return redirect('mis_obras')

    else:
        form = CrearObra(instance=obra)

    return render(request, 'perfil/editar_obra.html', {'form': form, 'obra': obra})

@login_required
def eliminar_obra(request, obra_id):
    obra = get_object_or_404(Obra, pk=obra_id)
    
    if request.user == obra.usuario or request.user.has_perm('polls.eliminar_obra'):
        if request.method == 'POST':
            obra.delete()
            return redirect('mis_obras')
        return render(request, 'perfil/eliminar_obra.html', {'obra': obra})
    else:
        pass

@login_required
def eliminar_capitulo(request, capitulo_id):
    capitulo = get_object_or_404(Capitulos, pk=capitulo_id)
    
    if request.user == capitulo.obra.usuario or request.user.has_perm('polls.eliminar_capitulo'):
        if request.method == 'POST':
            capitulo.delete()
            return redirect('capitulos_obra')
        return render(request, 'perfil/mis_obras/eliminar_capitulo.html', {'capitulo': capitulo})
    else:
        pass

@login_required
def capitulos_obra(request, obra_id):
    obra = get_object_or_404(Obra, pk=obra_id)

    if request.user != obra.usuario:
        return redirect('index')

    capitulos = obra.capitulos.all().order_by('orden')

    return render(request, 'perfil/mis_obras/capitulos_obra.html', {'obra': obra, 'capitulos': capitulos})

@login_required
def editar_capitulo(request, capitulo_id):
    capitulo = get_object_or_404(Capitulos, pk=capitulo_id)

    if request.user != capitulo.obra.usuario:
        return redirect('mis_obras')

    if request.method == 'POST':
        form = CapituloForm(request.POST, instance=capitulo)
        if form.is_valid():
            form.save()
            return redirect('mis_obras')

    else:
        form = CapituloForm(instance=capitulo)

    return render(request, 'perfil/mis_obras/editar_capitulo.html', {'form': form, 'capitulo': capitulo})

@login_required
def editar_perfil(request, username):
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil', username)
    else:
        form = PerfilUsuarioForm(instance=request.user)

    return render(request, 'perfil/editar_perfil.html', {'form': form})


def buscar_obras(request):
    query = request.GET.get('q')
    if query:
        resultados = Obra.objects.filter(
            Q(titulo__icontains=query) |
            Q(capitulos__contenido__icontains=query) |
            Q(usuario__username__icontains=query)
        ).distinct()
        print(resultados)
        return render(request, 'buscar_obras.html', {'obras': resultados, 'query': query})
    else:
        return render(request, 'buscar_obras.html', {'obras': None, 'query': None})

@csrf_exempt
@login_required
def like_capitulo(request, obra_id, capitulo_id):
    obra = get_object_or_404(Obra, id=obra_id)
    capitulo = get_object_or_404(Capitulos, id=capitulo_id, obra=obra)

    like, created = Like.objects.get_or_create(capitulo=capitulo, user=request.user)

    if not created:
        like.delete()

    like_count = capitulo.capitulo_likes.count()
    return JsonResponse({'like_count': like_count})

@login_required
def favoritos(request, username):
    user = Usuario.objects.get(username=username)
    
    user_likes_capitulos = Capitulos.objects.filter(capitulo_likes__user=user)
    
    user_likes_obras = Obra.objects.filter(capitulos__in=user_likes_capitulos).distinct()

    context = {
        'user_likes_obras': user_likes_obras,
    }

    return render(request, 'perfil/favoritos.html', context)