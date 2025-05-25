from django.contrib import admin
from django.urls import path # Keep path for admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Other app urls are now included in skill_path_recommender.urls
]

# Serve static files during development (keep this part)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)