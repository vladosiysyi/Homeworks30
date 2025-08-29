from django.urls import path
from .views import PaymentListAPIView,UserListView, UserDetailView

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
]
