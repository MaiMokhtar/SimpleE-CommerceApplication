import os
import sys
from pathlib import Path

import django

sys.path.append(str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

from _db_seed._profiles import UserProfileGenerator
from _db_seed._shopping import ItemGenerator


if __name__ == "__main__":
    print("Seeding database in progress...")

    UserProfileGenerator.create_user_profiles()
    UserProfileGenerator.create_user_profiles(cnt=1, is_superuser=True)
    ItemGenerator.create_items()

    print("Seeding is finished successfully!")
