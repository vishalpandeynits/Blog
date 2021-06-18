from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('status.urls', 'status'), namespace='status')),
    path('comments/', include('django_comments.urls')),
    path('create/',include('ckeditor_uploader.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)