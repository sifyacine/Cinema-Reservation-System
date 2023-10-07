from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registering/', include('authentication.urls')),
    path('movies/', include('cinema_houses.urls')),
]
