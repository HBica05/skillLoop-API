from django.contrib import admin
from django.urls import path, include
from users.views import api_root  # simple JSON "API is running" view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Root "status" endpoint (what you saw returning the JSON message)
    path("", api_root, name="api-root"),

    # Users app endpoints (register, contact, etc)
    path("api/", include("users.urls")),

    # Auth endpoints from dj-rest-auth
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
