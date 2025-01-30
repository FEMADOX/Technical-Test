import django_filters

from blogs.models import Note


class NoteFilter(django_filters.FilterSet):

    class Meta:
        model = Note
        fields = {
            "categories": ["exact"],
            "status": ["exact"],
        }
