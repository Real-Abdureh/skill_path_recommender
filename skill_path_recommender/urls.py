from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home # Assuming home view will be in accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # New home page URL
    path('accounts/', include('accounts.urls')),
    path('careers/', include('careers.urls')),
    path('learning-paths/', include('learning_paths.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)