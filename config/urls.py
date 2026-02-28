from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Бас бетке арналған функция
def home(request):
    return HttpResponse("Instagram Clone API жұмыс істеп тұр! Деректерді алу үшін /api/ мекенжайын қолданыңыз.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home), # Бас бетке функцияны қостық
    path('', include('pages.urls')),
]