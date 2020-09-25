from django.db import models


class Dictionary(models.Model):
    title = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "dictionary"
        verbose_name_plural = "dictionaries"


class Text(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    dictionary = models.ForeignKey(
        Dictionary,
        related_name='texts',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.title}"


class Token(models.Model):
    label = models.CharField(max_length=255)
    frequency = models.BigIntegerField(default=0)
    dictionary = models.ForeignKey(
        Dictionary,
        related_name='tokens',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.label}"

    class Meta:
        ordering = ['-frequency']
