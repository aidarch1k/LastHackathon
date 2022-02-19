from django.urls import path, include
from rest_framework.routers import SimpleRouter
from review.views import CommentViewSet

router = SimpleRouter()
router.register('comments', CommentViewSet, 'comments')

urlpatterns = [
    path('', include(router.urls)),
]
