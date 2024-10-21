from django.db import models

# Create your models here.
class RecentSearch(models.Model):
    city_name = models.CharField(max_length=100)
    search_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-search_date']

    def __str__(self):
        return self.city_name