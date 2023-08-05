from django.urls import path
from foodgram.urls import router

from .views import (
    DownloadShoppingCartView,
    FavoriteRecipeToUserView,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingCartToUserView,
    TagViewSet,
)


app_name = 'api'

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteRecipeToUserView.as_view(),
        name='favorite_recipe',
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartToUserView.as_view(),
        name='shopping_cart',
    ),
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCartView.as_view(),
        name='download_shopping_cart',
    ),
]
