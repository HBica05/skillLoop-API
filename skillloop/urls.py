from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def api_root(request):
    """
    Very simple health-check endpoint for /
    """
    return JsonResponse(
        {
            "message": "SkillLoop API is running",
            "endpoints": {
                "auth_login": "/dj-rest-auth/login/",
                "auth_register": "/dj-rest-auth/registration/",
                "contact": "/api/contact/",
            },
        }
    )


urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
]
