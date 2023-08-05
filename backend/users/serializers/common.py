from api.serializers import RecipeSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Follow
from users.serializers.nested import UserSerializer

User = get_user_model()


class FollowToSerializer(UserSerializer):
    """Сериализатор модели пользователя на странице подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes(self, obj):
        requests = self.context['request']
        recipes = obj.recipes.all()

        limit = requests.query_params.get('recipes_limit')
        if limit is not None:
            try:
                recipes = obj.recipes.all()[: int(limit)]
            except ValueError:
                pass

        fields = ('id', 'name', 'image', 'cooking_time')
        return RecipeSerializer(recipes, many=True, fields=fields).data

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FollowSerializer(serializers.ModelSerializer):
    """Сереиализатор для модели подписок."""

    follower = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Follow
        fields = ('follower', 'follow_to')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['follower', 'follow_to'],
                message='You are already a follower.',
            )
        ]

    def validate(self, attrs):
        if attrs['follow_to'] == attrs['follower']:
            raise serializers.ValidationError(
                'You cannot follow to yourself.',
            )
        return attrs
