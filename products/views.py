from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from products.models import Product,Review,Cart,ProductTag,FavoriteProduct
from products.serializers import ProductSerializer,ReviewSerializer,CartSerializer,ProductTagSerializer,FavoriteProductSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def product_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            product=serializer.save()
            return Response({"id":product.id},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_product(request,pk):
    product=get_object_or_404(Product,pk=pk)
    serializer=ProductSerializer(product)
    return Response(serializer.data) 


@api_view(['GET', 'POST'])
def review_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        review_list = []
        
        for review in reviews:
            review_data = {
                'id': review.id,
                'product_id': review.product.id,
                'content': review.content,
                'rating': review.rating
            }
            review_list.append(review_data)
        
        return Response({'reviews': review_list})

    elif request.method=='POST':
        serializer = ReviewSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            review = serializer.save()
            return Response(
                {'id': review.id, 'message': 'Review created successfully!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'POST'])
def cart_view(request):
    if not request.user.is_authenticated:
        return Response({"error": "authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method=='GET':
        user=request.user
        cart_items=Cart.objects.filter(user=user)
        serializer=CartSerializer(cart_items, many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            product=serializer.validated_data['product']
            quantity=serializer.validated_data['quantity']
            cart_item,created=Cart.objects.get_or_create(user=request.user,product=product)
            
            if not created:
                cart_item.quantity+=quantity
                cart_item.save()
            else:
                cart_item.quantity=quantity
                cart_item.save()

            return Response({"message": "Product added to cart"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def product_tag_view(request):
    if request.method=='GET':
        product_id=request.data.get('product_id')
        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "product not found"},status=status.HTTP_400_BAD_REQUEST)

        tags=ProductTag.objects.filter(product=product)
        serializer=ProductTagSerializer(tags,many=True)
        return Response(serializer.data)

    elif request.method=='POST':
        serializer=ProductTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Tag added successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def favorite_product_view(request):
    if not request.user.is_authenticated:
        return Response({"error": "authentication required."},status=status.HTTP_401_UNAUTHORIZED)

    if request.method=='GET':
        user=request.user
        favorite_products=FavoriteProduct.objects.filter(user=user)
        serializer=FavoriteProductSerializer(favorite_products, many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        serializer=FavoriteProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "product added to favorites"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)