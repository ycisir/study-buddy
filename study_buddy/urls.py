from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/', include('main.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.views.static import serve
# from django.urls import re_path

# urlpatterns += [
#     re_path(r'^static/(?P<path>.*)$', serve, {
#         'document_root': settings.MEDIA_ROOT,
#     }),
# ]