# LandHub/products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'), # Bỏ hoặc sửa nếu không dùng category
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # --- URLS MỚI CHO QUẢN LÝ TIN ĐĂNG ---
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/create/', views.create_listing, name='create_listing'),
    # Dùng <int:pk> thay vì id/slug cho edit/delete
    path('listing/<int:pk>/edit/', views.edit_listing, name='edit_listing'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('register/', views.register_view, name='register'),
    # ------------------------------------
]