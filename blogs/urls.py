from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blogs.views import (
    CategoryViewSet,
    NoteViewSet,
)

note_view_retrieve = NoteViewSet.as_view(
    actions={
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    },
)

router = DefaultRouter()
router.register(r"notes", NoteViewSet, "notes")
router.register(r"categories", CategoryViewSet, "category")

urlpatterns = [
    path("notes/note/<int:pk>", note_view_retrieve, name="note-detail"),
    path("", include(router.urls)),
]
