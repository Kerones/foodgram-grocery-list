from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from users.models import BaseModel

from .fields import HEXColorField
<<<<<<< HEAD
# from .managers import RecipeManager
=======
from .managers import RecipeManager
>>>>>>> e8d60c4fededb0deb138734d42bf4c9a50ed4a98

User = get_user_model()


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(unique=True, db_index=True, max_length=200)
    color = HEXColorField(unique=True)
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


<<<<<<< HEAD
# class MeasurementUnit(models.Model):
#     """Модель единиц измерения ингридиента."""

#     name = models.CharField(unique=True, max_length=30)

#     def __str__(self):
#         return self.name
=======
class MeasurementUnit(models.Model):
    """Модель единиц измерения ингридиента."""

    name = models.CharField(unique=True, max_length=30)

    def __str__(self):
        return self.name
>>>>>>> e8d60c4fededb0deb138734d42bf4c9a50ed4a98


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField(db_index=True, max_length=200)
<<<<<<< HEAD
    measurement_unit = models.CharField(max_length=200,
                                        verbose_name='Единица измерения')
=======
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.PROTECT,
    )
>>>>>>> e8d60c4fededb0deb138734d42bf4c9a50ed4a98

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient',
            ),
        ]

    def __str__(self):
        return self.name


class Recipe(BaseModel):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        db_index=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
    )
    name = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField()
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )

<<<<<<< HEAD
    # objects = RecipeManager()
=======
    objects = RecipeManager()
>>>>>>> e8d60c4fededb0deb138734d42bf4c9a50ed4a98

    class Meta:
        ordering = ('-created_at',)

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

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
        db_index=True,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'recipes_recipe_tags'
        verbose_name = 'tag'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_recipe_tag',
            ),
        ]


class RecipeIngredient(models.Model):
    """Связующая модель рецептов с ингридиентами."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        db_index=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )

    class Meta:
        db_table = 'recipes_recipe_ingredients'
        verbose_name = 'ingredient'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient',
            ),
        ]


class BaseRecipeToUser(BaseModel):
    """Базовая модель с полями пользователя и рецепта."""

    updated_at = None
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_%(class)s',
        db_index=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_%(class)s',
    )

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class FavoriteRecipe(BaseRecipeToUser):
    """Модель избранного."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe',
            ),
        ]


class ShoppingCart(BaseRecipeToUser):
    """Модель списка покупок."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart_recipe',
            ),
        ]
