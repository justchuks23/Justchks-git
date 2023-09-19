from django.urls import path
from .views import (
    ZoomVideoListView, AdminLoginView, AdminLogoutView,
    GetZoomVideoView, ZoomVideoDetailView, UploadDetailView
)

app_name = 'main'

urlpatterns = [
    path('', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', AdminLogoutView.as_view(), name='admin_logout'),
    path('<int:pk>/dashboard/', ZoomVideoListView.as_view(), name='home'),
    path('<int:pk>/zoom/', GetZoomVideoView.as_view(), name='user_zoom'),
    path('detail/<slug:slug>/', ZoomVideoDetailView.as_view(), name='detail'),
    path('<int:pk>/<slug:slug>/upload/', UploadDetailView.as_view(), name='upload'),
]
