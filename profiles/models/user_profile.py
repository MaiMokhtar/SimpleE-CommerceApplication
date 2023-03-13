from typing import Optional

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)


class UserProfileManager(BaseUserManager):
    """A custom manager for the UserProfile model that provides custom functionality for creating user objects."""

    def create_user(
        self,
        username: str,
        password: Optional[str] = None,
        *,
        commit: bool = True,
        **kwargs
    ) -> "UserProfile":
        """Creates a new user with the given username and password.

           Args:
               username: A string representing the username of the user to be created.
               password: An optional string representing the password of the user. If not provided,
                         a random, unusable password will be generated.
               commit: A boolean flag indicating whether to commit the user to the database immediately.
                       Defaults to True.
               **kwargs: Additional keyword arguments to pass to the user model constructor.

           Returns:
               A UserProfile instance representing the newly created user.

           Raises:
               ValueError: If username is empty or None.

           """
        if not username:
            raise ValueError("A user must have a username!")

        user = self.model(username=username, **kwargs)

        if not password:
            user.set_unusable_password()
        else:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def create_superuser(
        self,
        username: str,
        password: str,
        *,
        commit: bool = True
    ) -> "UserProfile":
        """Creates a new superuser with the given username and password.

           Args:
               username: A string representing the username of the superuser to be created.
               password: A string representing the password of the superuser.
               commit: A boolean flag indicating whether to commit the superuser to the database immediately.
                       Defaults to True.

           Returns:
               A UserProfile instance representing the newly created superuser.

           """
        return self.create_user(
            username=username,
            password=password,
            is_superuser=True,
            is_staff=True,
            commit=commit
        )


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """A custom user model with email and password as required fields.

    Attributes:
        username: A CharField representing the username of the user.
        is_active: A BooleanField indicating whether the user is active or not.
        is_superuser: A BooleanField indicating whether the user is a superuser or not.
        is_staff: A BooleanField indicating whether the user is staff or not.
        objects: A BaseUserManager instance used to manage the user model.
        USERNAME_FIELD: A string representing the name of the field to use for username.

    Methods:
        __str__: A method that returns the string representation of the user.
    """
    username: models.CharField = models.CharField(max_length=256, unique=True)
    is_active: models.BooleanField = models.BooleanField(default=True, null=False)
    is_superuser: models.BooleanField = models.BooleanField(default=False, null=False)
    is_staff: models.BooleanField = models.BooleanField(default=False, null=False)

    objects: BaseUserManager = UserProfileManager()
    USERNAME_FIELD: str = "username"

    def __str__(self) -> str:
        """Returns string representation for model object."""
        return str(self.username)
