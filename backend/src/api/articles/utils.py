import re


def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from a title.

    Args:
        title: The title to convert to a slug

    Returns:
        A lowercase string with spaces and special characters replaced with hyphens
    """
    # Convert to lowercase
    slug = title.lower()

    # Replace special characters with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", slug)

    # Remove leading/trailing hyphens
    slug = slug.strip("-")

    return slug
