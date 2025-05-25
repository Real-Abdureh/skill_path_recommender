"""
ASGI config for skill_path_recommender project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_path_recommender.settings')

application = get_asgi_application()