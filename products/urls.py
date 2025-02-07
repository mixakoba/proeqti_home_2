from django.urls import path
from products.views import ProductListCreateView,reviews_view,cart_view,product_tag_view,favorite_product_view,ProductDetailUpdateView

urlpatterns = [
    path('products/',ProductListCreateView.as_view(), name="products"),
    path('reviews/', reviews_view, name="reviews"),
    path('cart/',cart_view,name='cart_view'),
    path('product_tags/',product_tag_view,name='product_tag_view'),
    path('favorite_products/',favorite_product_view,name='favorite_product_view'),
    path('products/<int:pk>/',ProductDetailUpdateView.as_view(),name='product')
    
]