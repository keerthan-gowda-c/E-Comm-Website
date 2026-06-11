from django.urls import path
from . import views

urlpatterns = [
    path('',views.homeView, name = 'home_page'),
    path('about/', views.aboutView, name = 'about_page'),
    path('contact/', views.contactView, name = 'contact_page'),
   
    path('search', views.searchView, name = 'search_view'),

    path('carousels/', views.CarouselImageList.as_view(), name = 'carousel_page'),
    path('carousels/add/', views.AddCarouselImage.as_view(), name = 'add_carousel'),
    path('carousels/edit/<int:pk>/', views.UpdateCarouselImage.as_view(), name = 'edit_carousel'),
    path('carousels/del/<int:pk>', views.DeleteCarouselImage.as_view(), name='del_carousel')

]