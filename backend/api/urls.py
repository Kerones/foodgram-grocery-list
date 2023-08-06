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

from .views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                    ShoppingCartView, ShowSubscriptionsView, SubscribeView,
                    TagViewSet, download_shopping_cart)

app_name = 'api'

router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping_cart'
    ),
    path(
        'recipes/<int:id>/favorite/',
        FavoriteView.as_view(),
        name='favorite'
    ),
    path(
        'users/<int:id>/subscribe/',
        SubscribeView.as_view(),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        ShowSubscriptionsView.as_view(),
        name='subscriptions'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
