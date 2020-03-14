from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path("orders/", include('transactions.urls', namespace='transactions')),
    path('accounts/', include('accounts.urls')),
    
]

urlpatterns += staticfiles_urlpatterns()