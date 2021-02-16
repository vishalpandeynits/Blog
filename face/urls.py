from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('status.urls')),
    path('comments/', include('django_comments.urls')),
    path('create/',include('ckeditor_uploader.urls'))
]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)