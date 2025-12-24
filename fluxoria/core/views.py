from django.shortcuts import render, redirect
from django.db.models import Q

from posts.models import Post

import random

# Home
def home(request):
    posts = Post.objects.filter(
        is_published=True
    ).order_by('-created_at')

    # Filtro de nav (búsqueda)
    query = request.GET.get('q')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__profile__username__icontains=query)
        )

    # Filtro de nav (categorías)
    active_categories = request.GET.getlist('category')
    if active_categories:
        posts = posts.filter(category__in=active_categories)


    return render(request, 'core/home.html', {
        'posts': posts,
        'active_categories': active_categories,
        'query' : query,
    })


# Random Post
def random_post(request):
    qs = Post.objects.filter(is_published=True)

    count = qs.count()
    if count == 0:
        return redirect("core:home")

    post = qs[random.randint(0, count - 1)]
    return redirect("posts:detail", slug=post.slug)

def about_me(request):
    return render(request, "core/about_me.html")