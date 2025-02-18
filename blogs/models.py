from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    """
    Model representing a blog category.

    Variables:
        name: CharField
        description: TextField

    Returns:
        Model: Category
    """

    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class Note(models.Model):
    """Model representing a Note model

    Variables:
        title: CharField
        categories: ManyToManyField
        status: CharField
        content: TextField

    Returns:
        Model: Note
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=100)
    categories = models.ManyToManyField(
        Category,
        related_name="notes",
    )
    author = models.ForeignKey(
        User,
        related_name="notes",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        blank=True,
        default="active",
    )
    content = models.TextField(blank=True, default="NO CONTENT")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return f"Title: {self.title} - {self.status}"
