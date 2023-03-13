from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from profiles.models import UserProfile
from shopping.models import Item


class CartManager(models.Manager):
    """A custom manager for the Cart model.

    This manager provides a method for getting or creating a cart for a given user.

    """
    def get_or_create_by_user(self, user: UserProfile) -> "Cart":
        """Gets or creates a cart for a given user.

        Args:
            user: A UserProfile object representing the user to get or create a cart for.

        Returns:
            A Cart object representing the user's cart.

        """

        try:
            return user.cart
        except ObjectDoesNotExist:
            return self.create(user_profile=user)


class Cart(models.Model):
    """A model representing a user's shopping cart.

    Attributes:
        user_profile: A ForeignKey field linking to the UserProfile model representing the user who owns the cart.
        items: A ManyToManyField representing the items in the cart and their quantities.

    Properties:
        total_cost: An integer representing the total cost of all items in the cart.

    """
    user_profile: models.ForeignKey = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    items: models.ManyToManyField = models.ManyToManyField(Item, related_name="carts")

    objects = CartManager()

    @property
    def total_cost(self) -> int:
        """Calculates the total cost of all items in the cart.

        Returns:
            An integer representing the total cost of all items in the cart.

        """
        return self.items.aggregate(models.Sum("price"))["price__sum"] or 0

    def __str__(self) -> str:
        """Returns a string representation of the cart.

        Returns:
            A string representing the cart and its owner.

        """
        return f"{self.user_profile}'s cart"
