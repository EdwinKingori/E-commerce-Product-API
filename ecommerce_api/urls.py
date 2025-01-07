from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'E_CommerceProductAPI Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shopify/', include('shopify.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
