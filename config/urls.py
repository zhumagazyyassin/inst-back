from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # ОСЫ ЖЕР: 'admin.site.urls' болуы керек, 'admin.site.register' емес!
    path('', include('pages.urls')),
]