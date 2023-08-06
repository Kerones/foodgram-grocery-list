from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscription, User

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag,
                     ShoppingCart, Tag)


class CustomUserCreateSerializer(UserCreateSerializer):
    """ Сериализатор создания пользователя. """

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]


class CustomUserSerializer(UserSerializer):
    """ Сериализатор модели пользователя. """

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class TagSerializer(serializers.ModelSerializer):


<< << << < HEAD
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingridient."""


<< << << < HEAD
    # measurement_unit = serializers.StringRelatedField()
== == == =
    measurement_unit = serializers.StringRelatedField()
>>>>>> > e8d60c4fededb0deb138734d42bf4c9a50ed4a98

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для связующей таблицы Recipe и Ingridient."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )


== == == =
    """ Сериализатор просмотра модели Тег. """

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор модели, связывающей ингредиенты и рецепт. """

    id = serializers.ReadOnlyField(source='ingredient.id')


>>>>>> > v_1
    name = serializers.ReadOnlyField(source='ingredient.name')
<< << << < HEAD
    # measurement_unit = serializers.StringRelatedField(
    #     source='ingredient.measurement_unit',
    # )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
== == == =
    measurement_unit=serializers.StringRelatedField(
        source='ingredient.measurement_unit',
    )
    amount=serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
>>>>>> > e8d60c4fededb0deb138734d42bf4c9a50ed4a98
    )

    amount=serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
    )

    class Meta:
<< << << < HEAD
        model=Recipe.ingredients.through
        fields=('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""

    author=UserSerializer(default=serializers.CurrentUserDefault())
    image=Base64ImageField()
    ingredients=RecipeIngredientSerializer(
        many=True,
        allow_empty=False,
        source='recipe_ingredients',
    )
    tags=CustomPKRelatedField(
        many=True,
        allow_empty=False,
        queryset=Tag.objects.all(),
        serializer_repr_class=TagSerializer,
    )
    cooking_time=serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
    )
    is_favorited=SerializerMethodField()
    is_in_shopping_cart=SerializerMethodField()

    class Meta:
        model=Recipe
        exclude=('created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        fields=kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed=set(fields)
            existing=set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_is_favorited(self, obj):
        return getattr(obj, 'in_favorite_recipe', False)

    def get_is_in_shopping_cart(self, obj):
        return getattr(obj, 'in_shopping_cart', False)

    def validate_ingredients(self, value):
        checked_values=[]
        for element in value:
            if (ingredient_obj := element['ingredient']) in checked_values:
                error_detail={
                    'id': [f'Ingredient "{ingredient_obj.name}" is repeated.'],
                }
                raise serializers.ValidationError([error_detail])
            checked_values.append(ingredient_obj)
        return value
== == == =
        model=RecipeIngredient
        fields=['id', 'name', 'amount', 'measurement_unit']


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор просмотра модели Ингредиенты. """

    class Meta:
        model=Ingredient
        fields=['id', 'name', 'measurement_unit']


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор просмотра модели Рецепт. """

    tags=TagSerializer(many=True)
    author=CustomUserSerializer(read_only=True)
    ingredients=serializers.SerializerMethodField()
    is_favorited=serializers.SerializerMethodField(
        method_name='get_is_favorited')
    is_in_shopping_cart=serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart')

    class Meta:
        model=Recipe
        fields=[
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

    def get_ingredients(self, obj):
        ingredients=RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request=self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request=self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe_id=obj
        ).exists()


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор добавления ингредиента в рецепт. """

    id=serializers.IntegerField()
    amount=serializers.IntegerField()

    class Meta:
        model=RecipeIngredient
        fields=['id', 'amount']


class CreateRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор создания/обновления рецепта. """

    author=CustomUserSerializer(read_only=True)
    ingredients=AddIngredientRecipeSerializer(many=True)
    tags=serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image=Base64ImageField()

    class Meta:
        model=Recipe
        fields=[
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]

    def validate(self, data):
        ingredients=self.initial_data.get('ingredients')
        list=[]
        for i in ingredients:
            amount=i['amount']
            if int(amount) < 1:
                raise serializers.ValidationError({
                    'amount': 'Количество ингредиента должно быть больше 0!'
                })
            if i['id'] in list:
                raise serializers.ValidationError({
                    'ingredient': 'Ингредиенты должны быть уникальными!'
                })
            list.append(i['id'])
        return data

    def create_ingredients(self, ingredients, recipe):
        for i in ingredients:
            ingredient=Ingredient.objects.get(id=i['id'])
            RecipeIngredient.objects.create(
                ingredient=ingredient, recipe=recipe, amount=i['amount']
            )
>> >>>> > v_1

    def create_tags(self, tags, recipe):
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)

    def create_tags(self, tags, recipe):
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)

    def create(self, validated_data):
<< << << < HEAD
        tags=validated_data.pop('tags')
        ingredients=validated_data.pop('recipe_ingredients')

        instance=self.Meta.model.objects.create(**validated_data)
        self._set_tags(instance, tags)
        self._set_ingredients(instance, ingredients)

        return instance

    def update(self, instance, validated_data):
        tags=validated_data.pop('tags', None)
        ingredients=validated_data.pop('recipe_ingredients', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags:
            self._set_tags(instance, tags)
        if ingredients:
            self._set_ingredients(instance, ingredients)

        return instance

    def _set_tags(self, instance, tags):
        instance.tags.set(tags)

    def _set_ingredients(self, instance, ingredients):
        instance.ingredients.clear()
        IngredientsThrough=self.Meta.model.ingredients.through
        IngredientsThrough.objects.bulk_create(
            [
                IngredientsThrough(recipe=instance, **ingredient)
                for ingredient in ingredients
            ]
        )


class RecipeToUserSerializerMixin(serializers.Serializer):
    """Mixin serializer. Included `user` and `recipe` fields."""

    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    recipe=serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        fields=('user', 'recipe')

    def to_representation(self, instance):
        fields=('id', 'name', 'image', 'cooking_time')
        return RecipeSerializer(instance.recipe, fields=fields).data


class FavoriteRecipeSerializer(
    RecipeToUserSerializerMixin, serializers.ModelSerializer
):
    """Сериализатор для модели FavoriteRecipe."""

    class Meta:
        model=FavoriteRecipe
        fields=RecipeToUserSerializerMixin.Meta.fields
        validators=[
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['user', 'recipe'],
                message='The recipe has already been added to favorites.',
            ),
        ]


class ShoppingCartSerializer(
    RecipeToUserSerializerMixin, serializers.ModelSerializer
):
    """Сериализатор для модели Cart."""

    class Meta:
        model=ShoppingCart
        fields=RecipeToUserSerializerMixin.Meta.fields
        validators=[
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['user', 'recipe'],
                message=(
                    'The recipe has already been added to the shopping cart.'
                ),
            ),
        ]
== == == =
        """
        Создание рецепта.
        Доступно только авторизированному пользователю.
        """

        ingredients=validated_data.pop('ingredients')
        tags=validated_data.pop('tags')
        author=self.context.get('request').user
        recipe=Recipe.objects.create(author=author, **validated_data)
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        """
        Изменение рецепта.
        Доступно только автору.
        """

        RecipeTag.objects.filter(recipe=instance).delete()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        ingredients=validated_data.pop('ingredients')
        tags=validated_data.pop('tags')
        self.create_ingredients(ingredients, instance)
        self.create_tags(tags, instance)
        instance.name=validated_data.pop('name')
        instance.text=validated_data.pop('text')
        if validated_data.get('image'):
            instance.image=validated_data.pop('image')
        instance.cooking_time=validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class ShowFavoriteSerializer(serializers.ModelSerializer):
    """ Сериализатор для отображения избранного. """

    class Meta:
        model=Recipe
        fields=['id', 'name', 'image', 'cooking_time']


class ShoppingCartSerializer(serializers.ModelSerializer):
    """ Сериализатор для списка покупок. """

    class Meta:
        model=ShoppingCart
        fields=['user', 'recipe']

    def to_representation(self, instance):
        return ShowFavoriteSerializer(instance.recipe, context={
            'request': self.context.get('request')
        }).data


class FavoriteSerializer(serializers.ModelSerializer):
    """ Сериализатор модели Избранное. """

    class Meta:
        model=Favorite
        fields=['user', 'recipe']

    def to_representation(self, instance):
        return ShowFavoriteSerializer(instance.recipe, context={
            'request': self.context.get('request')
        }).data


class ShowSubscriptionsSerializer(serializers.ModelSerializer):
    """ Сериализатор для отображения подписок пользователя. """

    is_subscribed=serializers.SerializerMethodField()
    recipes=serializers.SerializerMethodField()
    recipes_count=serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=[
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        request=self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj).exists()

    def get_recipes(self, obj):
        request=self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipes=Recipe.objects.filter(author=obj)
        limit=request.query_params.get('recipes_limit')
        if limit:
            recipes=recipes[:int(limit)]
        return ShowFavoriteSerializer(
            recipes, many=True, context={'request': request}).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализатор подписок. """

    class Meta:
        model=Subscription
        fields=['user', 'author']
        validators=[
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author'],
            )
        ]

    def to_representation(self, instance):
        return ShowSubscriptionsSerializer(instance.author, context={
            'request': self.context.get('request')
        }).data
>> >>>> > v_1
