from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Ingredient(models.Model):
    """ Модель ингредиента. """

    name = models.CharField(
        'Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='ingredient_name_unit_unique'
            ),
        )


class Tag(models.Model):
    """ Модель тега. """

    name = models.CharField('Название тега', unique=True, max_length=200)
    color = models.CharField('Цвет', unique=True, max_length=7)
    slug = models.SlugField('Slug', unique=True, max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Модель рецепта. """

    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги',
        related_name='tags'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/'
    )
    name = models.CharField('Название рецепта', max_length=200)
    text = models.TextField(
        'Описание рецепта',
        help_text='Введите описание рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator(
            1, message='Время приготовления должно быть не менее 1 минуты!'
        ),)
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name

    def _get_old_image(self):
        if self.pk is None:
            return None
        try:
            return self.__class__.objects.get(pk=self.pk).image
        except self.__class__.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        old_image = self._get_old_image()
        save_result = super().save(*args, **kwargs)
        if old_image is not None and old_image != self.image:
            old_image.delete(save=False)
        return save_result

    def delete(self, *args, **kwargs):
        delete_result = super().delete(*args, **kwargs)
        self.image.delete(save=False)
        return delete_result


class RecipeTag(models.Model):
    """Связующая модель рецептов с тегами."""

class RecipeIngredient(models.Model):
    """ Модель связи ингредиента и рецепта. """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество',
        validators=(MinValueValidator(1),)
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='recipe_ingredient_unique'
            ),
        )


class RecipeTag(models.Model):
    """ Модель связи тега и рецепта. """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'tag'),
                name='recipe_tag_unique'
            ),
        )


class ShoppingCart(models.Model):
    """ Модель корзины. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_shoppingcart_unique'
            ),
        )


class Favorite(models.Model):
    """ Модель избранного. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_favorite_unique'
            ),
        )
