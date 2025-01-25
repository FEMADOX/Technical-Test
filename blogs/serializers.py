from rest_framework import serializers

from blogs.models import Category, Note


class CategorySerializer(serializers.ModelSerializer):

    class Meta:  # type: ignore[misc]
        model = Category
        fields = ["name"]


class NoteSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:  # type: ignore[misc]
        model = Note
        fields = ["title", "categories", "content", "status"]


class CategoryNoteSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True)

    class Meta:  # type: ignore[misc]
        model = Category
        fields = ["name", "notes"]
