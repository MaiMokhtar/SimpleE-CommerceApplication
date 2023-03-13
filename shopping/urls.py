from django.urls import path

from shopping.views import PurchaseView, CartConfirmView, CartItemRemoveView, OrderListView

app_name = "shopping"
urlpatterns = [
    path("", PurchaseView.as_view(), name="purchase"),
    path("cart/confirm/", CartConfirmView.as_view(), name="cart-confirm"),
    path("cart/items/<int:item_id>/remove", CartItemRemoveView.as_view(), name="cart-item-remove"),
    path("orders/", OrderListView.as_view(), name="order-list")
]
