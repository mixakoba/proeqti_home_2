from rest_framework import serializers
from products.models import Review, Product,Cart,ProductTag,FavoriteProduct
from users.models import User


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    currency = serializers.ChoiceField(choices=['GEL', 'USD', 'EUR'])


class ReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    content = serializers.CharField()
    rating = serializers.IntegerField()

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data['product_id'])
        user = self.context['request'].user

        review = Review.objects.create(
            product=product,
            user=user,
            content=validated_data['content'],
            rating=validated_data['rating'],
        )
        return review
    
class CartSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name',read_only=True)

    class Meta:
        model=Cart
        fields=['id', 'product', 'product_name', 'quantity']

    def validate_quantity(self,value):
        if value<=0:
            raise serializers.ValidationError("quantity must be a positive integer")
        return value

    def validate_product(self,value):
        try:
            product=Product.objects.get(id=value.id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("product does not exist")
        return value
    
class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductTag
        fields=['id','product','tag_name']

    def validate_tag_name(self, value):
        product_id=self.initial_data.get('product_id')
        if ProductTag.objects.filter(product_id=product_id, tag_name=value).exists():
            raise serializers.ValidationError("this tag already exist for this product.")
        return value

    def validate_product(self, value):
        try:
            product=Product.objects.get(id=value.id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("product does not exist")
        return value
    
class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=FavoriteProduct
        fields=['id','user','product']

    def validate_product(self, value):
        try:
            product=Product.objects.get(id=value.id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("product does not exist")
        return value

    def validate_user(self, value):
        try:
            user=User.objects.get(id=value.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        return value