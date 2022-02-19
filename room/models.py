from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


ROOM_STATUS = (
    ('VIP', 'Вип'),
    ('Luxury', 'Люкс'),
    ('Economy', 'Эконом')
)


class Room(models.Model):
    name = models.CharField('Название', max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField('Картинка', upload_to='Pictures')
    desc = models.TextField()
    price = models.DecimalField('Цена', max_digits=100, decimal_places=2)
    is_reserved = models.BooleanField('Бронь', default=False)
    number_of_people = models.PositiveIntegerField('Количество людей')
    status = models.CharField('Статус комнаты', max_length=10, choices=ROOM_STATUS)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return self.name


class Reservation(models.Model):
    check_in = models.DateField(default=timezone.now())
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='Комната')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Посетитель')

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def rating_avg(self):
        avg = 0
        rating = Rating.objects.filter(room=self)
        for rate in rating:
            avg += rate.mark
        if len(rating) > 0:
            return avg / len(rating)
        else:
            return 0


class Rating(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.DecimalField(validators=[MinValueValidator(1), MaxValueValidator(5)], max_digits=50,
                               decimal_places=1, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = (('user', 'room'),)
        index_together = (('user', 'room'),)


class Like(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    is_liked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Favorite(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='favorite_pub')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)


