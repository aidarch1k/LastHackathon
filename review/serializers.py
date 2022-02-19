from rest_framework import serializers


from review.models import Comment
from room.models import Room


class CommentSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Room.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'room', 'text', 'user',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
