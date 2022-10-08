from django.urls import path
from item.views import ItemView

urlpatterns = [
    path('admin/item', ItemView.as_view()),
]
