from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Bucket, Product
from products.serializers import BucketSerializer, ProductSerializers


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_permissions(self):
        if self.action in ['create', 'delete', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class BucketModelViewSet(ModelViewSet):
    queryset = Bucket.objects.all()
    serializer_class = BucketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response({'product_id': 'Not existing'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Bucket.create_or_update(products.first().id, request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
            # return super().create(request, *args, **kwargs)
        except KeyError:
            return Response({'product_id': 'required'}, status=status.HTTP_400_BAD_REQUEST)
