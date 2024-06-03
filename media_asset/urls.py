from django.urls import path
from . import views

urlpatterns = [
    path('post-assets/', views.CreateAssetAPIView.as_view(), name='post_assets'),
    path('list-assets/', views.AssetListAPIView.as_view(), name="list_assets"),
    path('asset/<int:pk>/', views.AssetRetrieveUpdateAPIView.as_view(), name='update_retrieve_asset'),
    path('asset/search/', views.AssetSearchAPIView.as_view(), name='asset_search'),
]
