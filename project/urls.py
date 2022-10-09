from django.urls import path

from actor.views import AdminActorView
from editor.views import AdminEditorView
from item.views import ItemView, AdminItemView, AdminItemCheckView, AdminItemUpdateView

urlpatterns = [
    path('items', ItemView.as_view()),
    path('admin/actors', AdminActorView.as_view()),
    path('admin/editors', AdminEditorView.as_view()),
    path('admin/items', AdminItemView.as_view()),
    path('admin/items/<int:pk>', AdminItemUpdateView.as_view()),
    path('admin/items/<int:pk>/check', AdminItemCheckView.as_view())
]
