from django.urls import path
from products.views import product_view,review_view,cart_view,product_tag_view,favorite_product_view,get_product

urlpatterns = [
    path('products/<int:pk/', product_view, name="products"),
    path('reviews/', review_view, name="reviews"),
    path('cart/',cart_view,name='cart_view'),
    path('product_tags/',product_tag_view,name='product_tag_view'),
    path('favorite_products/',favorite_product_view,name='favorite_product_view'),
    path('products/<int:pk>/',get_product,name='product')
    
]