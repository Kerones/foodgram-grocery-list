from django.urls import path
from foodgram.urls import router

from .views import FollowToListView, FollowView, UserViewSet

app_name = 'users'

router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path(
        'users/subscriptions/',
        FollowToListView.as_view(),
        name='follow-list',
    ),
    path(
        'users/<int:follow_to_id>/subscribe/',
        FollowView.as_view(),
        name='follow',
    ),
]
