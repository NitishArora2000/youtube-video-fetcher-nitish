from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_default = models.URLField()
    thumbnail_medium = models.URLField()
    thumbnail_high = models.URLField()

    class Meta:
        indexes = [
            models.Index(fields=['published_at'], name='published_at_idx'),
            models.Index(fields=['title', 'description'], name='title_desc_idx'),
        ]

    def __str__(self):
        return self.title
