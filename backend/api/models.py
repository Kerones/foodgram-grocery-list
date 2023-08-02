from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from string import hexdigits

User = get_user_model()


class Tag(models.Model):
    NAME_LIMIT = 15
    name = models.CharField(
        verbose_name="Тег",
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name="Цвет",
        max_length=7,
        unique=True,
        db_index=False,
    )
    slug = models.CharField(
        verbose_name="Слаг тега",
        max_length=50,
        unique=True,
        db_index=False,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:self.NAME_LIMIT]

    def hex_validator(color):
        color = color.strip(' #')
        if len(color) not in (3, 6):
            raise ValidationError(
                f'Код цвета {color} имеет некорректную длину: ({len(color)}).'
            )
        if not set(color).issubset(hexdigits):
            raise ValidationError(f'{color} не является шестнадцатиричным.')
        if len(color) == 3:
            return f'#{color[0] * 2}{color[1] * 2}{color[2] * 2}'.upper()
        return '#' + color.upper()

    def clean(self):
        self.name = self.name.strip().lower()
        self.slug = self.slug.strip().lower()
        self.color = self.hex_validator(self.color)
        return super().clean


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ('name',)
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
    text = models.TextField('Текстовое описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        related_name='recipes',
        through='IngredientAmount',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )

    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        editable=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=1,
        validators=(MinValueValidator(
            1,
            message='Время приготовления блюда не может быть меньше минуты'),
            MaxValueValidator(
            32767,
            message='Время приготовления блюда не может быть таким долгим')
        ))

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингридиент',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(MinValueValidator(
            1,
            message='Чтобы приготовить блюдо нужен хотя бы один ингридиент'),
            MaxValueValidator(
            32767, message='Слишком много ингридиентов!')
        ))

    class Meta:
        ordering = ('-recipe',)
        verbose_name = 'Количества ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique ingredients recipe'
            )
        ]


class CustomModel(models.Model):
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique recipe in favorites'
            ),
        ]


class Favorite(CustomModel):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Cart(CustomModel):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты',
        on_delete=models.CASCADE,
        related_name='cart',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='follower',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='following',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]
