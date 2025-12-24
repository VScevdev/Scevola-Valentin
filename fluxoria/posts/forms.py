from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=Post.CATEGORY_CHOICES,
        required=False,
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'thumbnail']
        labels = {
            'title' : 'Título',
            'content' : 'Contenido',
            'category' : 'Categoría',
            'thumbnail' : 'Imagen/Miniatura',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input'
            }),
            'content': forms.Textarea(attrs={
                'class': 'textarea',
                'rows' : 8
            }),
            'category': forms.Select(attrs={
                'class': 'select'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'file-input',
                'accept': 'image/*'
            }),
        }

    def clean_thumbnail(self):
        image = self.cleaned_data.get('thumbnail')

        if image:
            max_size = 32 * 1024 * 1024  # 32MB
            if image.size > max_size:
                raise forms.ValidationError("La imagen no puede pesar más de 32MB.")

        return image