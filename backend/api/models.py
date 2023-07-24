from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
    )

    class Meta:
        ordering = [-'id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
    )
    metric = models.CharField(
        'Единица измерения',
        max_length=200
    )

    class Meta:
        ordering = [-'id']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название',
        max_length=200,
    )
    image = models.ImageField(
        'Фото',
        upload_to='media/',
    )
    description = models.TextField('Текстовое описание')
    ingridients = models.ManyToManyField(
        'Ингридиенты',
        related_name='recipes',
        to=Ingridient,
        through='IngridientAmount',
    )
    tags = models.ManyToManyField(
        'Теги',
        related_name='recipes',
        to=Tag,
    )

    pud_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        editable=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=1,
        validators=validators.MinValueValidator(
            1, message='Проверьте Ваши часы!'
        )
    )

    class Meta:
        ordering = [-'id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngridientAmount(models.Model):
    ingridient = models.ForeignKey(
        'Ингридиент',
        Ingridient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Рецепт',
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=validators.MinValueValidator(
            1, message='Требуется хотя бы один ингридиент!'
        )
    )

    class Meta:
        ordering = [-'id']
        verbose_name = 'Количества ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique ingredients recipe'
            )
        ]


class Favorite(models.Model):
    recipe = models.ForeignKey(
        'Рецепты',
        related_name='favorites',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'Пользователь',
        related_name='favorites',
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique recipe in favorites'
            ),
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        'Владелец',
        User,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    recipe = models.ForeignKey(
        'Рецепт',
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique recipe in cart',
            )
        ]
