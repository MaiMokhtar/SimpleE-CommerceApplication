from shopping.models import Item


class ItemGenerator:
    """Class representing an item generator."""
    @staticmethod
    def create_items(cnt: int = 10) -> None:
        """Static method that creates one or more items.

        Args:
            cnt: The number of items to create. Default is 10.
        """
        items = []
        for i in range(cnt):
            items.append(Item(name=f"Item #{i + 1}", price=(i + 1) * 10))
        Item.objects.bulk_create(items)
