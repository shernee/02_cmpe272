from django.db import models

class Tweet(models.Model):
    """A tweet."""
    tweet_id = models.CharField(max_length=255)
    text = models.CharField(max_length=280)
    date_added = models.DateTimeField(blank=True, null=True)
    author_id = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=255, blank=True)

    
    def __str__(self):
        """Return a string representation of the model."""
        return self.text[:50] + "..."