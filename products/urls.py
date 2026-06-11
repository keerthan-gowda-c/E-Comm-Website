from django.urls import path
from . import views


urlpatterns = [
    # Product CRUD path
    path('', views.ProductList.as_view(), name = 'product_list'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name = 'product_details'),
    path('add/', views.AddProduct.as_view(), name = 'add_product'),
    path('edit/<int:pk>', views.UpdateProduct.as_view(), name = 'edit_product'),
    path('del/<int:pk>', views.DeleteProduct.as_view(), name = 'del_product'),
    
    path('product/<int:pk>/add-image/', views.AddProductImageView.as_view(), name='add_product_image'),
    path('image/<int:pk>/edit/', views.UpdateProductImage.as_view(), name = 'edit_product_image'),
    path('image/<int:pk>/del/', views.DeleteProductImage.as_view(), name = 'del_product_image'),

    # Category CRUD
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/add/', views.AddCategory.as_view(), name='add_category'),
    path('categories/edit/<int:pk>/', views.UpdateCategory.as_view(), name='edit_category'),
    path('categories/delete/<int:pk>/', views.DeleteCategory.as_view(), name='delete_category'),

    # Filter by category
    path('category/<int:pk>/products/', views.ProductList.as_view(), name='category_products'),
   
]