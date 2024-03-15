from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('book.urls')),
    path('', include('order.urls')),
    path('', include('support.urls')),
    path('authors/', include('author.urls'))
]
