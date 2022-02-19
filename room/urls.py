from django.urls import path, include
from rest_framework.routers import SimpleRouter
from room.views import *


router = SimpleRouter()
router.register('room', RoomViewSet, 'room',)
router.register('rate', RatingViewSet, 'rating',)


urlpatterns = [
    path('', include(router.urls)),
    path('saved/', FavoriteView.as_view()),
    path('confirm/', ReservationView.as_view()),
]