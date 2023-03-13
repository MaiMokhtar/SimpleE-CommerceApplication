from typing import Hashable, Any, Optional, Union

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View, ListView

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import notifications.constants
from shopping.forms.purchase import PurchaseForm
from shopping.models import Cart
from shopping.models.order import Order


@method_decorator(login_required, name='dispatch')
class PurchaseView(TemplateView):
    """Renders a purchase form and handles form submission for adding items to the user's cart.

    Only accessible to authenticated users.

    Attributes:
        template_name: The name of the HTML template used to render the purchase form.

    Methods:
        get_context_data(**kwargs): Overrides the parent method to add a `PurchaseForm` instance to the context.

        post(request: HttpRequest) -> Union[HttpResponse, HttpResponsePermanentRedirect]: Handles form submission,
        adds the selected items to the user's cart, and redirects to the cart confirmation page on success.

    """
    template_name = "shopping/purchase.html"

    def get_context_data(self, **kwargs) -> dict[Hashable, Any]:
        """Overrides the parent method to add a `PurchaseForm` instance to the context.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict[Hashable, Any]: The updated context.
        """
        context = super(PurchaseView, self).get_context_data(**kwargs)
        return context | {"purchase_form": PurchaseForm()}

    def post(self, request: HttpRequest) -> Union[HttpResponse, HttpResponsePermanentRedirect]:
        """Handles form submission, adds the selected items to the user's cart, and redirects to the cart
           confirmation page on success.

        Args:
            request: The HTTP request object.

        Returns:
            Union[HttpResponse, HttpResponsePermanentRedirect]: A redirect to the cart confirmation page on success
                                                                or a rendered purchase form on error.
        """
        purchase_form = PurchaseForm(request.POST)

        if not purchase_form.is_valid():
            return render(
                request=request,
                context={
                    "purchase_form": purchase_form
                },
                template_name=self.template_name
            )

        cart = Cart.objects.get_or_create_by_user(request.user)
        to_be_added = [
            cart.items.through(cart=cart, item=item)
            for item in purchase_form.cleaned_data["items"]
            if item not in cart.items.all()
        ]
        cart.items.through.objects.bulk_create(to_be_added)

        return redirect("shopping:cart-confirm")


@method_decorator(login_required, name='dispatch')
class CartConfirmView(TemplateView):
    """View class that handles the cart confirmation process for a user.

    Attributes:
        template_name: The name of the HTML template that the view should render.

    Methods:
        get(request, *args, **kwargs): Ensure to initialize a cart for the user.
        post(request): Process payment, create a new order, flush the cart, and send a notification to the user.

    """
    template_name = "shopping/cart_confirm.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Ensure to initialize a cart for the user.

        Args:
            request: The HTTP request object.
            args: Positional arguments passed to the method.
            kwargs: Keyword arguments passed to the method.

        Returns:
            A `TemplateResponse` object that renders the HTML template with the initialized cart.
        """
        Cart.objects.get_or_create_by_user(request.user)
        return super(CartConfirmView, self).get(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponsePermanentRedirect:
        """Process payment, create a new order, flush the cart, and send a notification to the user.

        Args:
            request: The HTTP request object.

        Returns:
            A `HttpResponsePermanentRedirect` object that redirects the user to the purchase page.
        """
        # Process payment should be added here.

        # Create a new order.
        order = Order.objects.create(user_profile=request.user)
        order.items.set(request.user.cart.items.all())

        request.user.cart.items.set([])  # Flush the cart contents.

        # Send a notification.
        async_to_sync(get_channel_layer().group_send)(
            notifications.constants.NOTIFICATIONS_GROUP_NAME_PREFIX + request.user.username,
            {
                "type": "notify",  # Custom Function written in the consumers.py
                "message": "A new order was placed successfully!",
            },
        )

        return redirect("shopping:purchase")


@method_decorator(login_required, name='dispatch')
class CartItemRemoveView(UserPassesTestMixin, View):
    """A view for removing an item from the user's shopping cart.

    Only superusers are allowed to remove items from a cart. Once an item is removed, the user will be redirected to the
    cart confirmation page.

    """
    def test_func(self) -> Optional[bool]:
        """Tests if the user is a superuser.

       Returns:
           bool: True if the user is a superuser, otherwise False.
       """
        return self.request.user.is_superuser

    def post(self, request: HttpRequest, item_id: int) -> HttpResponsePermanentRedirect:
        """Removes an item from the user's shopping cart and redirects the user to the cart confirmation page.

        Args:
            request: The request object.
            item_id: The ID of the item to remove.

        Returns:
            HttpResponsePermanentRedirect: A redirect to the cart confirmation page.
        """
        request.user.cart.items.remove(item_id)
        return redirect("shopping:cart-confirm")


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    """View to display a list of orders for the authenticated user.

    Attributes:
        model: The model used to retrieve the orders (Order).
        context_object_name: The name of the context variable containing the orders (orders).
        template_name: The name of the template used to render the view (shopping/order_list.html).

    Methods:
        get_queryset: Override the base method to filter orders by the user's profile.

    """
    model = Order
    context_object_name = "orders"
    template_name = "shopping/order_list.html"

    def get_queryset(self) -> QuerySet:
        """Overrides the base method to filter orders by the user's profile.

       Returns:
           A queryset of orders filtered by the user's profile.

       """
        return Order.objects.filter(user_profile=self.request.user)
