from django.core.validators import RegexValidator


class HEXColorValidator(RegexValidator):
    """Валидация Hex-кода для цвета тэга."""

    regex = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
