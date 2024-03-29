from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_default = models.URLField()
    thumbnail_medium = models.URLField()
    thumbnail_high = models.URLField()

    # Add other fields as needed

    def __str__(self):
        return self.title
