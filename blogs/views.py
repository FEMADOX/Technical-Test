from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from blogs.models import Category, Note
from blogs.serializers import (
    CategoryNoteSerializer,
    CategorySerializer,
    NoteSerializer,
)

# Create your views here.


class NoteListView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_object(self) -> Note:
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get("note_id")

        return get_object_or_404(queryset, pk=lookup_value)


class NoteStatusView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self) -> QuerySet[Note]:
        queryset = self.get_queryset().filter(status=self.kwargs.get("status"))
        error = "No notes found with this status"

        if queryset:
            return queryset

        raise Http404(error)


class CategoryNoteView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryNoteSerializer
    lookup_url_kwarg = "category_id"


class CategoryNoteCreateDeleteView(generics.GenericAPIView):
    serializer_class = CategoryNoteSerializer

    @classmethod
    def post(cls, request: Request) -> Response:
        note_id = request.data.get("note_id")
        category_id = request.data.get("category_id")
        note = get_object_or_404(Note, pk=note_id)
        category = get_object_or_404(Category, pk=category_id)
        note.categories.add(category)
        note.save()

        return Response(
            {"status": "category added to note"},
        )

    @classmethod
    def delete(cls, request: Request) -> Response:
        note_id = request.data.get("note_id")
        category_id = request.data.get("category_id")
        note = get_object_or_404(Note, pk=note_id)
        category = get_object_or_404(Category, pk=category_id)
        note.categories.remove(category)
        note.save()

        return Response(
            {"status": "category removed from note"},
            status=status.HTTP_204_NO_CONTENT,
        )
