from rest_framework import serializers
from room.models import Room,Favorite, Rating, Reservation
from review.serializers import CommentSerializer


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes_count'] = instance.likes.count()
        return rep


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['likes_count'] = instance.likes.count()
        return rep


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class FavoriteRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

        def get_favorite(self, obj):
            if obj.is_favorite:
                return obj.is_favorite
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['favorites'] = self.get_favorite(instance)
            return rep


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

        def get_reservation(self, obj):
            if obj.is_reservation:
                return obj.is_reservation
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['reservation'] = self.get_reservation(instance)
            return rep


class RatingSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Room.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

    def validate(self, attrs):
        room = attrs.get('room')
        request = self.context.get('request')
        user = request.user
        if Rating.objects.filter(room=room, user=user).exists():
            raise serializers.ValidationError('Вы уже голосовали')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
