from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """AppConfig class for the 'profiles' app.

    Attributes:
        default_auto_field: A string representing the name of the field to use for the default auto primary key field.
        name: A string representing the name of the app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
