from django.urls import include, path
from rest_framework import routers

from api.views import BucketModelViewSet, ProductModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('products', ProductModelViewSet)
router.register('products', BucketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
