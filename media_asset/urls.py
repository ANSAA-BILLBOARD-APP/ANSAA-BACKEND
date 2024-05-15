from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.TaskAPIView.as_view(), name="assigned_asset"),
    path('post-assets/', views.CreateAssetAPIView.as_view(), name='post_assets'),
    path('list-assets/', views.AssetListAPIView.as_view(), name="list_assets"),
    path('asset/<int:pk>/', views.AssetRetrieveUpdateAPIView.as_view(), name='update_retrieve_asset'),
]
