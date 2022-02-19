from django.contrib.auth import get_user_model
from django.db import models
from room.models import Room


User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.room} от {self.user}'
