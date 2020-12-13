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
    tagged_text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    token_statistics = models.JSONField(null=True)

    dictionary = models.ForeignKey(
        'Dictionary',
        related_name='texts',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.title}"


class Token(models.Model):
    label = models.CharField(max_length=255)
    frequency = models.BigIntegerField(default=0)
    tags = models.ManyToManyField(
        'Tag',
        related_name='tokens',
    )
    dictionary = models.ForeignKey(
        'Dictionary',
        related_name='tokens',
        on_delete=models.CASCADE,
    )
    lemma = models.OneToOneField(
        'Lemma',
        related_name='token',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.label}"

    class Meta:
        ordering = ['-frequency']
        unique_together = (
            ('label', 'dictionary')
        )


class Lemma(models.Model):
    """
    Store the base form of the token
    """
    label = models.CharField(max_length=255)
    tag = models.ForeignKey(
        'Tag',
        related_name='lemmas',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.label} - {self.tag}"


class Tag(models.Model):
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    examples = models.TextField()

    def __str__(self):
        return f"{self.code}"

    class Meta:
        ordering = ['code']
