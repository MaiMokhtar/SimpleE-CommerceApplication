from django.apps import AppConfig


class ShoppingConfig(AppConfig):
    """AppConfig class for the 'shopping' app.

    Attributes:
        default_auto_field: A string representing the name of the field to use for the default auto primary key field.
        name: A string representing the name of the app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopping'
