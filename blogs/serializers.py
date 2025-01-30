from rest_framework import serializers

from blogs.models import Category, Note


class CategorySerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore[misc]
        model = Category
        fields = ["name"]


class NoteSerializer(serializers.ModelSerializer):
    note = serializers.HyperlinkedIdentityField(
        view_name="note-detail",
        lookup_field="pk",
        read_only=True,
    )
    categories = CategorySerializer(many=True)

    class Meta:  # type: ignore[misc]
        model = Note
        fields = ["note", "title", "categories", "content", "status"]


class CategoryNoteSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:  # type: ignore[misc]
        model = Category
        fields = ["name", "notes"]
