from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """
    Simple JSON response so we can see that the API is alive on Heroku.
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
    # Root of the site: https://skillloop-35d5850f8d20.herokuapp.com/
    path("", api_root, name="api-root"),

    # Admin
    path("admin/", admin.site.urls),

    # Your app’s API endpoints
    path("api/", include("users.urls")),

    # Auth endpoints (login/logout/password etc.)
    path("dj-rest-auth/", include("dj_rest_auth.urls")),

    # Registration endpoints
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
]
