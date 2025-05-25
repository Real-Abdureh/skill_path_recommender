from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Home and account management urls
    path('', include('accounts.urls')),
    # Career exploration
    path('careers/', include('careers.urls')),
    # Learning paths
    path('learning-paths/', include('learning_paths.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)