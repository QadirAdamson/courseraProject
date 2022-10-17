from django.urls import path
from courseraScrap import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', home),
    path('<str:category>/', get_data),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)