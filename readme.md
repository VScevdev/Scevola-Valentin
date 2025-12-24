# Fluxoria

---

## Objetivo funcional del proyecto

El objetivo de Fluxoria es desarrollar una aplicación web que permita a sus usuarios realizar posteos de diferentes categorías, 
    en la búsqueda de la creación de una comunidad artística (y expansible a otras áreas en un futuro).

## Descripción general del sistema

Fluxoria es una aplicación web organizada en múltiples apps para mantener una arquitectura modular y escalable, la intención es realizar en un futuro un deploy del proyecto utilizando esta Entrega Final como base. Por este motivo, se priorizó una arquitectura modular y escalable.

El sistema permite:
- Crear, editar y eliminar posts (solo usuarios autenticados).
- Asociar cada post a un autor.
- Filtrar por búsqueda y/o categorías los posts.
- Visualizar los posts.
- Gestionar perfiles de usuario de forma automática.
- Gestionar perfiles públicos de manera manual.
- Suscribirse a posts y/o artistas (no implementado aún).
- Visualizar un Top temporal de posteos según valoraciones de otros usuarios (no implementado aún).
- Visualizar videos y reproducir música (no implementado aún).

---

## Apps del proyecto

- **core**:  
  Home y navegación básica. 
  Feed de Posts.
  Apartado de autenticación/registro.
  Funciones de crear posts deshabilitadas (ocultas y con acceso restringido).

- **accounts**:  
  Gestión de usuarios, autenticación y backend personalizado de login (email o username).

- **profiles**:  
  Manejo del perfil de usuario, incluyendo username público, bio, país y avatar.

- **posts**:  
  Lógica principal de creación, edición, visualización y eliminación de publicaciones.

---

## Modelos del sistema

### User (accounts)

Modelo de usuario personalizado basado en `AbstractBaseUser`.

Campos principales:
- `email` (único, usado para login)
- `is_active`
- `is_staff`
- `date_joined`

---

### Profile (profiles)

Perfil asociado uno a uno con cada usuario.

Campos principales:
- `user` (OneToOneField)
- `username` (canónico, único, guardado en db)
- `username_display`
- `country`
- `bio`
- `avatar`
- `onboarding_completed`
- `created_at`

El perfil se crea automáticamente al crear un usuario mediante señales.
El onboarding está pensado para usuarios creados desde el panel de administración o desde la terminal, y no forma parte del flujo principal de registro del usuario común.

---

### Post (posts)

Representa una publicación creada por un usuario.

Campos principales:
- `title`
- `slug` (generado automáticamente)
- `content`
- `category`
- `thumbnail` (imagen opcional)
- `author` (ForeignKey a User)
- `is_published`
- `created_at`
- `updated_at`

Cada post pertenece a un único autor.

---

## Autenticación

El sistema utiliza un backend de autenticación personalizado que permite iniciar sesión utilizando:
- Email del usuario
- Username público del perfil

---

## Control de acceso

- La creación, edición y eliminación de posts requiere que el usuario esté autenticado.
- Solo el autor de un post puede editarlo o eliminarlo.
- Los usuarios no autenticados solo pueden visualizar posts publicados.

---

## Testing

Se implementaron tests básicos utilizando el sistema de testing de Django para validar el correcto funcionamiento del sistema.

Los tests cubren:
- Carga de la página principal
- Restricción de acceso a usuarios no autenticados
- Creación de posts
- Generación automática de slug
- Creación automática del perfil de usuario

Los casos de test están documentados en el archivo **Casos de Test.xls**.

---

## Usuario administrador

Para acceder al panel de administración de Django:

- Usuario: coderhouse.python@test.com
- Contraseña: entregafinal.scevola

