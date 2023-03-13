from django.db import models

from profiles.models import UserProfile
from shopping.models import Item


class Order(models.Model):
    """Represents an order made by a user.

    Attributes:
        user_profile: The user who made the order.
        items: The items that were ordered.
        created_at: The timestamp when the order was created.
    """
    user_profile: models.ForeignKey = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    items: models.ManyToManyField = models.ManyToManyField(Item, related_name="orders")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self) -> int:
        """Calculates the total cost of the order.

        Returns:
            int: The total cost in USD.
        """
        return self.items.aggregate(models.Sum("price"))["price__sum"] or 0

    def __str__(self) -> str:
        """Returns a string representation of the order.

        Returns:
            str: A string representation of the order.
        """
        return f"{self.user_profile}'s order"
