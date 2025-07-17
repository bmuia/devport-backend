from django.urls import path
from .views import AccessTokenGenerateView, AppCreateView, AppListView, AccessTokenListView

urlpatterns = [
    path('apps/', AppListView.as_view(), name='list-apps'),
    path('apps/create/', AppCreateView.as_view(), name='create-app'),
    path('token/', AccessTokenGenerateView.as_view(), name='generate-token'),
    path('tokens/list/', AccessTokenListView.as_view(), name='list-tokens')
]
