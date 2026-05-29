from django.urls import path
from . import views

urlpatterns = [

    path('index/', views.home, name='index'),

    path('home/', views.home_page, name='home'),

    path('signup/', views.signup_view, name='signup'),

    path('', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('upload-paint/', views.upload_paint, name='upload_paint'),

    path('delete-paint/<int:paint_id>/', views.delete_paint, name='delete_paint'),

    path('paints/', views.paint_list, name='paint_list'),

    path('admin-users/', views.admin_users, name='admin_users'),

    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('colors/', views.color_list, name='colors'),

    path('colors/<str:color_name>/', views.color_paints, name='color_paints'),

# CART
path(
    'cart/',
    views.cart_view,
    name='cart'
),

path(
    'cart/add/<int:paint_id>/',
    views.add_to_cart,
    name='add_to_cart'
),

path(
    'cart/remove/<int:cart_id>/',
    views.remove_cart,
    name='remove_cart'
),


# INCREASE QTY
path(
    'cart/increase/<int:cart_id>/',
    views.increase_quantity,
    name='increase_quantity'
),

# DECREASE QTY
path(
    'cart/decrease/<int:cart_id>/',
    views.decrease_quantity,
    name='decrease_quantity'
),

# urls.py
# BUY NOW
path(
    'buy/<int:id>/',
    views.buy_now,
    name='buy_now'
),

# CHECKOUT
path(
    'checkout/',
    views.checkout,
    name='checkout'
),

# PLACE ORDER
path(
    'place-order/',
    views.place_order,
    name='place_order'
),

# PAYMENT SUCCESS
path(
    'payment-success/',
    views.payment_success,
    name='payment_success'
),

# ORDERS
path(
    'orders/',
    views.orders,
    name='orders'
),



    path('wishlist/add/<int:paint_id>/', views.add_to_wishlist, name='add_to_wishlist'),

    

    path('paint/<int:id>/', views.paint_detail, name='paint_detail'),
    
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

]