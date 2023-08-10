from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag

EMPTY = '-пусто-'


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through


class TagsInLine(admin.TabularInline):
    model = Recipe.tags.through


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'user__email')
    empty_value_display = EMPTY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = EMPTY


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorites')
    search_fields = ('name', 'author__username')
    list_filter = ('tags',)
    empty_value_display = EMPTY
    inlines = (
        IngredientsInLine,
        TagsInLine,
    )

    def favorites(self, obj):
        if Favorite.objects.filter(recipe=obj).exists():
            return Favorite.objects.filter(recipe=obj).count()
        return 0


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user__username', 'user__email')
    empty_value_display = EMPTY


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = EMPTY
