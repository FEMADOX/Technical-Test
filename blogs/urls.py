from django.urls import path

from blogs.views import (
    CategoryListView,
    CategoryNoteCreateDeleteView,
    CategoryNoteView,
    NoteDetailView,
    NoteListView,
    NoteStatusView,
)

urlpatterns = [
    path("notes/", NoteListView.as_view(), name="note-list"),
    path("notes/<str:status>/", NoteStatusView.as_view(), name="notes-by-status"),
    path("note/<int:note_id>/", NoteDetailView.as_view(), name="note-detail"),
    path("categories/", CategoryListView.as_view(), name="categories-list"),
    path(
        "category/<int:category_id>/",
        CategoryNoteView.as_view(),
        name="category-notes",
    ),
    path(
        "note-categories/",
        CategoryNoteCreateDeleteView.as_view(),
        name="category-note-create-delete",
    ),
]
