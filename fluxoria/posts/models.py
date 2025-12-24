from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True
    )

    content = models.TextField()

    CATEGORY_CHOICES = [
        ('uncategorized', 'Sin categoría'),
        ('music', 'Música'),
        ('art', 'Arte'),
        ('video', 'Video'),
        ('writing', 'Escritos'),
        ('games', 'Juegos'),        
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='uncategorized',
        blank=True,
    )

    thumbnail = models.ImageField(
        upload_to='posts/thumbnails/',
        blank=True,
        null=True
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )



    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "post"
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
