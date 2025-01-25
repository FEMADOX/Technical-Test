from django.db import models

# Create your models here.


class Category(models.Model):
    """
    Model representing a blog category.
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
    """
    Model representing a Note.
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
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default="active",
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return f"Title: {self.title} - {self.status}"
