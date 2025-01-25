from rest_framework import serializers

from blogs.models import Category, Note


class CategorySerializer(serializers.BaseSerializer):

    class Meta:
        model = Category
        fields = ["name"]


class NoteSerializer(serializers.BaseSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Note
        fields = ["title", "categories", "content", "status"]


class CategoryNoteSerializer(serializers.BaseSerializer):
    notes = NoteSerializer(many=True)

    class Meta:
        model = Category
        fields = ["name", "notes"]
