from rest_framework import serializers
from products.models import Review, Product,Cart,ProductTag,FavoriteProduct
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField(write_only=True)

    class Meta:
        model=Review
        fields=['product_id', 'content', 'rating']

    def validate_product_id(self,value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid product_id. Product does not exist.")
        return value

    def validate_rating(self,value):
        if value<1 or value>5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self,validated_data):
        product=Product.objects.get(id=validated_data.pop('product_id'))
        user=self.context['request'].user
        return Review.objects.create(product=product,user=user,**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(many=True, read_only=True)
    class Meta:
        exclude=['created_at', 'updated_at', 'tags'] 
        model=Product
    
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