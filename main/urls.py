from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'),  # New URL pattern for delete view
]
