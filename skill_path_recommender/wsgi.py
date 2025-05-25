"""
WSGI config for skill_path_recommender project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skill_path_recommender.settings')

application = get_wsgi_application()