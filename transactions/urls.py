from django.urls import path
from . import views

app_name = 'transactions'
urlpatterns = [
    path('', views.orders_list, name='list'),

    path('new/', views.new_order, name='new_order'),
    path('new_order_created/<uuid:access_code>', views.new_order_created, name='new_order_created'),

    path('order/<uuid:access_code>/', views.order, name='order'),
    path('edit/<uuid:access_code>/', views.OrderEditView.as_view(), name='edit_order'),
    path('delete/<uuid:access_code>/', views.OrderDeleteView.as_view(), name='delete_order'),

    path('find_order/', views.find_order, name='find_order'),

    path('<uuid:access_code>/payment/', views.payment, name='payment'),
]
