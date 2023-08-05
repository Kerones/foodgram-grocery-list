from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import permissions, views, viewsets
from users.paginations import PageNumberLimitPagination

from .filters import IngredientFilter, RecipeFilter
from .mixins import BaseRecipeToUserView
from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели тегов."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели ингридиентов."""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.select_related('measurement_unit')
    permission_classes = (permissions.AllowAny,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для модели рецептов."""

    serializer_class = RecipeSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly,)
    pagination_class = PageNumberLimitPagination
    filterset_class = RecipeFilter

    def get_queryset(self):
        return Recipe.objects.setup_eager_loading(self.request.user)


class FavoriteRecipeToUserView(BaseRecipeToUserView):
    """View для создания и удаления избранных рецептов."""

    serializer_class = FavoriteRecipeSerializer
    queryset = FavoriteRecipe.objects.all()
    list_name = 'favorites list'


class ShoppingCartToUserView(BaseRecipeToUserView):
    """View для создания и удаления списка покупок."""

    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    list_name = 'shopping cart'


class DownloadShoppingCartView(views.APIView):
    """View для скачивания списка покупок."""

    file_name = 'shopping_cart_list.txt'
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.get_content(), headers=self.get_headers())

    def get_headers(self):
        return {
            'Content-Type': 'text/plain',
            'Content-Disposition': f'attachment; filename="{self.file_name}"',
        }

    def get_content(self):
        queryset = self.get_queryset()
        content = '\n'.join(self.create_simple_ingredient_list(queryset))
        return content

    def get_queryset(self):
        user = self.request.user
        queryset = Ingredient.objects.filter(
            recipeingredient__recipe__in_shoppingcart__user_id=user.id
        ).annotate(amount=Sum('recipeingredient__amount'))
        return queryset

    def create_simple_ingredient_list(self, ingredients_qs):
        simple_ingredient_list = [
            f"{obj.name} ({obj.measurement_unit.name}) — {obj.amount}"
            for obj in ingredients_qs
        ]
        return simple_ingredient_list
