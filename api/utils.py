from django.contrib.auth.models import User

def generate_aub_id():
    """
    Generates ID like: AUB20250001
    """
    year = 2025  # or use datetime.now().year

    count = User.objects.filter(username__startswith=f"AUB{year}").count() + 1

    return f"AUB{year}{count:04d}"
