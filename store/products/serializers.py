from rest_framework import fields, serializers

from products.models import Bucket, Product, ProductCategory


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'qty', 'img', 'category']

    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=ProductCategory.objects.all()
    )


class BucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket
        fields = ['id', 'product', 'qty', 'created_at', 'sum', 'total_sum']
        read_only_field = ['created_at']

    product = ProductSerializers()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_qty = fields.SerializerMethodField()

    def get_total_sum(self, obj):
        return Bucket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_qty(self, obj):
        return Bucket.objects.filter(user_id=obj.user.id).total_qty()
