from rest_framework import serializers

from blogs.models import Category, Note


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:  # type: ignore[misc]
        model = Category
        fields = ["id", "name"]


class NoteSerializer(serializers.ModelSerializer):
    note_url = serializers.HyperlinkedIdentityField(
        view_name="note-detail",
        lookup_field="pk",
        read_only=True,
    )
    categories = CategorySerializer(many=True)

    class Meta:  # type: ignore[misc]
        model = Note
        fields = ["note_url", "title", "categories", "content", "status"]


class CategoryNoteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:  # type: ignore[misc]
        model = Category
        fields = ["id", "name", "notes"]
