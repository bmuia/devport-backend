from django.urls import path
from .views import GenerateToken,CreateAppView

urlpatterns = [
    path('generate-token/', GenerateToken.as_view(),name='generate-token'),
    path('create/', CreateAppView.as_view(), name='create-app'),
]
