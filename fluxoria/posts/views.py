from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Post
from .forms import PostCreateForm

# Post Abierto

def post_detail(request, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True
    )

    return render(request, 'posts/post_detail.html', {
        'post': post
    })

# Crear Post

@login_required(login_url='accounts:login')
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:detail', slug=post.slug)
    else:
        form = PostCreateForm()

    return render(request, 'posts/post_form.html', {'form': form})

# Editar Post

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        return HttpResponseForbidden("No tenés permiso para editar este post.")

    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', slug=post.slug)
    else:
        form = PostCreateForm(instance=post)

    return render(request, 'posts/post_form.html', {
        'form': form,
        'post': post,
        'is_edit': True,
    })

# Borrar Post

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        return HttpResponseForbidden("No tenés permiso para borrar este post.")

    if request.method == 'POST':
        post.delete()
        return redirect('core:home')

    return render(request, 'posts/post_confirm_delete.html', {
        'post': post
    })
