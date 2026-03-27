from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from pages.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Авторизация және Токен
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Барлық кестелер (pages/urls.py ішіндегі жолдар)
    path('api/', include('pages.urls')),
]