from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from ninja import NinjaAPI
from Meetings.api import router as schuzky_router

api = NinjaAPI()
api.add_router("/v1/", schuzky_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("NovyProjekt.urls")),
    path('Meetings/', include('Meetings.urls')),
    path('api/', api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
