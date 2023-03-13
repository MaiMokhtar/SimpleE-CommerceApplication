from profiles.models import UserProfile


class UserProfileGenerator:
    """Class representing a user profile generator."""
    @staticmethod
    def create_user_profiles(cnt: int = 1, is_superuser: bool = False) -> None:
        """Static method that creates one or more user profiles.

        Args:
            cnt: The number of user profiles to create. Default is 1.
            is_superuser: Whether to create user profiles with superuser privileges. Default is False.
        """
        user_profiles = []
        username_prefix = "superuser" if is_superuser else "auto_generated"
        for i in range(cnt):
            user_profiles.append(
                UserProfile.objects.create_user(
                    username=f"{username_prefix}_{i + 1}",
                    password="new_password",
                    commit=False,
                    is_superuser=is_superuser,
                    is_staff=is_superuser
                )
            )
        UserProfile.objects.bulk_create(user_profiles)
