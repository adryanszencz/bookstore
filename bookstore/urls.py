from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from bookstore import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("update_server/", views.update_server, name="update_server"),
    path("hello/", views.hello_world, name="hello_world"),
    path("api-auth/", include("rest_framework.urls")),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("bookstore/v1/", include("product.urls")),
    path("bookstore/v1/", include("order.urls")),
]

if settings.DEBUG and not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
