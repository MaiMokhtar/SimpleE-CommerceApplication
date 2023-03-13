from django.db import models


class Item(models.Model):
    """Represents an item that can be purchased in the online store.

    Attributes:
        name: The name of the item.
        price: The price of the item in USD.

    """

    name: models.CharField = models.CharField(max_length=256, blank=False, null=False)
    price: models.IntegerField = models.IntegerField(blank=False, null=False)

    def __str__(self) -> str:
        """Returns a string representation of the item, including its name and price.

        Returns:
            str: A string representation of the item.
        """
        return f"{self.name} ({self.price} USD)"
