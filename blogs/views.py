from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from blogs.filters import NoteFilter
from blogs.models import Category, Note
from blogs.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from blogs.serializers import (
    CategoryNoteSerializer,
    NoteSerializer,
)

# Create your views here.


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = NoteFilter
    filter_backends = [DjangoFilterBackend]

    def create(self, request: Request) -> Response:
        title = request.data.get("title")
        categories_data = request.data.get("categories")
        content = request.data.get("content")
        status_data = request.data.get("status")

        if categories_data:
            category_list = [category["id"] for category in categories_data]
            categories = Category.objects.filter(id__in=category_list)
            new_note = Note.objects.create(
                title=title,
                content=content,
                status=status_data,
            )
            new_note.categories.set(categories)

            serializer = NoteSerializer(new_note, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "categories required"},
            status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request: Request, pk: int) -> Response:
        note = get_object_or_404(Note, pk=pk)
        title = request.data.get("title")
        categories_data = request.data.get("categories")
        content = request.data.get("content")
        status_data = request.data.get("status")

        if categories_data is not None and title:
            try:
                category_list = [category["id"] for category in categories_data]
                categories = Category.objects.filter(id__in=category_list)
            except KeyError:
                category_list = [category["name"] for category in categories_data]
                categories = Category.objects.filter(name__in=category_list)
            note.title = title
            note.categories.set(categories)
            note.content = content or note.content
            note.status = status_data or note.status
            note.save()

            serializer = NoteSerializer(note, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        note.title = ""
        note.categories.clear()
        note.content = ""
        note.status = "active"

        serializer = NoteSerializer(note, context={"request": request})
        return Response(
            serializer.data,
            status.HTTP_200_OK,
        )

    def partial_update(self, request: Request, pk: int) -> Response:
        note = get_object_or_404(Note, pk=pk)
        title = request.data.get("title")
        categories_data = request.data.get("categories")
        content = request.data.get("content")
        status_data = request.data.get("status")

        if (
            not any([title, categories_data, content, status_data])
            and categories_data != []
        ):
            return Response(
                {"detail": "Please provide at least one field to patch"},
                status.HTTP_400_BAD_REQUEST,
            )

        if title and note.title != title:
            note.title = title
        if categories_data is not None:
            try:
                category_list = [category["id"] for category in categories_data]
                categories = Category.objects.filter(id__in=category_list)
            except KeyError:
                category_list = [category["name"] for category in categories_data]
                categories = Category.objects.filter(name__in=category_list)

            # Are the categories of the note the same as the categories in the request?
            current_categories = set(note.categories.values_list("pk", flat=True))
            new_categories = set(categories.values_list("pk", flat=True))
            if current_categories != new_categories:
                note.categories.set(categories)
        elif categories_data == []:
            note.categories.clear()
        if content and note.content != content:
            note.content = content
        if status_data and note.status != status_data:
            note.status = status_data
        note.save()

        serializer = NoteSerializer(note, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryNoteSerializer
    permission_classes = [IsAdminOrReadOnly]
