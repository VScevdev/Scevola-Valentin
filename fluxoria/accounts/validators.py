import re
from django.core.exceptions import ValidationError

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002700-\U000027BF"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE
)

def validate_username(value: str):
    # longitud
    if len(value) > 24:
        raise ValidationError("El nombre de usuario no puede superar los 24 caracteres.")

    # emojis
    if EMOJI_PATTERN.search(value):
        raise ValidationError("El nombre de usuario no puede contener emojis.")

    # contar letras reales
    letters = re.findall(r"[a-zA-Z]", value)
    if len(letters) < 4:
        raise ValidationError(
            "El nombre de usuario debe contener al menos 4 letras (a–z)."
        )