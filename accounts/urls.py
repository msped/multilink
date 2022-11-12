from django.urls import path, include

from .views import BlacklistTokenView, ChangePasswordView, CustomTokenObtainPairView

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
    path('jwt/token/', CustomTokenObtainPairView.as_view(), name="obtain_token_pair"),
    path('jwt/blacklist/', BlacklistTokenView.as_view(), name="logout"),
    path(
        'change-password/',
        ChangePasswordView.as_view(),
        name="change_password"
    ),
]