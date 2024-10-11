from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('shop/', views.shop, name='shop'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('product-detail/<int:pk>', views.productdetail, name='product-detail'),
    path('logout/', views.logout, name='logout'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('cart_close', views.cart_close, name='cart_close'),
    path('checkout', views.checkout, name='checkout'),
    path('check_out', views.check_out, name='check_out'),
    path('order', views.order, name='order'),
    path('about/', views.about, name='about'),

]