from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from blogs.models import Note


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return User.objects.get(pk=request.user.pk).is_staff
        except User.DoesNotExist:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return self.has_object_permission(
            request,
            view,
            Note(),
        )

    def has_object_permission(self, request: Request, view: APIView, obj: Note) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            user = User.objects.get(pk=request.user.pk)
            obj = Note.objects.get(pk=view.kwargs.get("pk"))
            return obj.author == user or user.is_staff
        except User.DoesNotExist:
            return False
