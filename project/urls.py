from django.contrib import admin
from django.urls import path
from django.urls import re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from actor.views import AdminActorView
from editor.views import AdminEditorView
from item.views import ItemView, AdminItemView, AdminItemCheckView, AdminItemUpdateView


schema_url_patterns = [
    path('items', ItemView.as_view()),
    path('admin/actors', AdminActorView.as_view()),
    path('admin/editors', AdminEditorView.as_view()),
    path('admin/items', AdminItemView.as_view()),
    path('admin/items/<int:pk>', AdminItemUpdateView.as_view()),
    path('admin/items/<int:pk>/check', AdminItemCheckView.as_view())
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Open API",
        default_version='v1',
        description="시스템 API",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('items', ItemView.as_view()),
    path('admin/actors', AdminActorView.as_view()),
    path('admin/editors', AdminEditorView.as_view()),
    path('admin/items', AdminItemView.as_view()),
    path('admin/items/<int:pk>', AdminItemUpdateView.as_view()),
    path('admin/items/<int:pk>/check', AdminItemCheckView.as_view())
]
