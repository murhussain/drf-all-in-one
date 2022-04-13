from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movie.api.urls')),
    path('', include('users.api.urls')),
    # path('api-auth', include('rest_framework.urls'))
]
