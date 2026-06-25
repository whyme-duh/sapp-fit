import os

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from dotenv import load_dotenv
load_dotenv()

from django.conf.urls.static import static

urlpatterns = [
    path('', include('website.urls')),
    path("__reload__/", include("django_browser_reload.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns.append(
        path('admin/', admin.site.urls),
    )
else:
    urlpatterns.append(
        path(os.environ.get('ADMIN_URL', 'admin/'), admin.site.urls),
    )



handler404 = 'website.views.page_not_found_404'
handler500 = 'website.views.page_not_found_500'