from django.contrib import admin
from django.urls import path, include
from scuser.views import index, RegisterView, LoginView, logout
from product.views import ProductList,ProductCreate,ProductDetail,ProductListAPI,ProductDetailAPI
from order.views import OrderCreate, OrderList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('register/',RegisterView.as_view()),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', logout,name='logout'),
    path('product/',ProductList.as_view(),name ='productList'),
    path('product/<int:pk>/',ProductDetail.as_view()),
    path('product/create/',ProductCreate.as_view(),name ='productCreate'),
    path('order/',OrderList.as_view(),name='order'),
    path('order/create/',OrderCreate.as_view(),name='orderCreate'),

    path('api/product/',ProductListAPI.as_view()),
    path('api/product/<int:pk>/',ProductDetailAPI.as_view()),


]
