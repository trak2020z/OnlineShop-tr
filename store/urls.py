from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path("", views.index, name="index"),
    
    path("products/", views.product_list, name='list'),
    path('products/<str:cat>', views.product_list, name='list'),

    path("product/<int:product_id>/", views.product_details, name='details'),

    path('cart/', views.cart, name='cart'),

    path("add_one/", views.add_one, name="add_one"),
    path("set_amount/", views.set_amount, name="set_amount"),
    path("remove_all/", views.remove_all, name="remove_all"),
]
