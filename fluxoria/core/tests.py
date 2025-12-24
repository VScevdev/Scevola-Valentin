from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Post
from profiles.models import Profile

User = get_user_model()

class BasicProjectTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="12345678"
        )

    # 1️⃣ Home carga correctamente
    def test_home_page_loads(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)

    # 2️⃣ Crear post requiere login
    def test_create_post_requires_login(self):
        response = self.client.get(reverse("posts:create"))
        self.assertNotEqual(response.status_code, 200)

    # 3️⃣ Usuario logueado puede crear post
    def test_logged_user_can_create_post(self):
        Post.objects.create(
            title="Post test",
            content="Contenido de prueba",
            category="uncategorized",
            author=self.user
        )
    
        self.assertEqual(Post.objects.count(), 1)
    # 4️⃣ El slug se genera automáticamente
    def test_post_slug_is_generated(self):
        post = Post.objects.create(
            title="Post de Prueba",
            content="Texto",
            author=self.user
        )
        self.assertIsNotNone(post.slug)

    # 5️⃣ Al crear usuario se crea su Profile
    def test_profile_is_created_with_user(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

