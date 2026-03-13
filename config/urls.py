from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # LOGIN ЖҮЙЕСІ (Postman-да: /api/token/)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ҚОЛДАНБА СІЛТЕМЕЛЕРІ
    path('api/', include('pages.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]