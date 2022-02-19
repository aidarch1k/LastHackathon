from datetime import datetime, timedelta
from django_filters import rest_framework as rfilter
from room.models import Room, Like, Favorite, Rating, Reservation
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, generics, viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet
from room.permissions import IsAuthorOrIsAdmin, IsAuthor
from room.serializers import RoomListSerializer, RoomDetailSerializer, \
    CreateRoomSerializer, FavoriteRoomSerializer, RatingSerializer, ReservationSerializer


class RoomFilter(rfilter.FilterSet):
    created_at = rfilter.DateTimeFromToRangeFilter()

    class Meta:
        model = Room
        fields = ('created_at',)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer
    permission_classes = [IsAuthorOrIsAdmin,]
    filter_backends = [rfilter.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RoomFilter
    search_fields = ['name','price', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListSerializer
        elif self.action == 'retrieve':
            return RoomDetailSerializer
        return CreateRoomSerializer

    @action(['POST','DELETE'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(room=post, user=user)
            like.is_liked = not like.is_liked
            if like.is_liked:
                like.save()
            else:
                like.delete()
            message = 'Нрпвится' if like.is_liked else 'Вам больше не нравится эта запись'
        except Like.DoesNotExist:
            Like.objects.create(room=post, user=user, is_liked=True)
            message = 'Нравится'
        return Response(message, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            favorite = Favorite.objects.get(room=post, user=user)
            favorite.is_favorite = not favorite.is_favorite
            if favorite.is_favorite:
                favorite.save()
            else:
                favorite.delete()
            message = 'В избранном' if favorite.is_favorite else 'Не в избранном'
        except Favorite.DoesNotExist:
            Favorite.objects.create(room=post, user=user, is_favorite=True)
            message = 'В избранном'
        return Response(message, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def confirm(self, request, pk=None):
        if request.method == 'POST':
            if pk:
                room_id = Room.objects.get(pk=pk)
                guest_id = request.user
                check_in = request.data['check_in']
                check_out = request.data['check_out']
                reservation = Reservation(check_in=check_in, check_out=check_out, room_id=room_id.id,
                                          guest_id=guest_id.pk)
                reservation.save()
                book_in = datetime.strptime(check_in, '%Y-%m-%d').date()
                book_out = datetime.strptime(check_out, '%Y-%m-%d').date()
                reserved = False
                delta = timedelta(days=1)
                while book_in <= book_out:
                    room_id.reserved = True
                    book_in += delta
                else:
                    room_id.reserved = False
        data = ReservationSerializer(reservation).data
        return Response(data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return []
        elif self.action in ['like', 'favorite', 'reservation']:
            return [IsAuthenticated()]
        else:
            return []


class FavoriteView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteRoomSerializer
    filter_backends = [rfilter.DjangoFilterBackend]
    filterset_fields = ['user']


class ReservationView(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [rfilter.DjangoFilterBackend]
    filterset_fields = ['guest']


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]

