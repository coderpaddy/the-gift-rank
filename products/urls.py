from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name='index'),
    path('gift/<category>', views.categorydetail, name='category'),
    path('gift/<category>/<rank>', views.productdetail, name='product'),
    path('add/new', views.addProduct, name='addproduct'),
    
]