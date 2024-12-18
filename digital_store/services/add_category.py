from digital_store.models import Category


CATEGORIES = [
    {
        "name": "Courses",
        "description": "Online courses and educational materials for self-education and professional growth",
    },
    {
        "name": "E-books",
        "description": "Digital editions of books on any topic: from fiction to professional reference books",
    },
    {
        "name": "Graphic content",
        "description": "Templates, graphics and fonts for designers and creative professionals",
    },
    {
        "name": "Music",
        "description": "Audio tracks and music albums for inspiration and entertainment",
    },
    {
        "name": "Photo content",
        "description": "Professional photographs and image collections for various projects",
    },
    {
        "name": "Podcasts",
        "description": "Interesting podcasts on current topics from authors from all over the world",
    },
    {
        "name": "Software",
        "description": "Programs, utilities and applications for solving problems in various fields",
    },
    {
        "name": "Video content",
        "description": "Video materials, including clips and videos, for personal and commercial use",
    },
    {
        "name": "Video games and in-game content",
        "description": "Digital games and add-ons, including in-game items and bonuses",
    },
]


def add_category(categories: list[dict]) -> None:
    category_objects = [Category(**category) for category in categories]
    Category.objects.bulk_create(category_objects)

    print("Categories added successfully")
