from django.db import models


# Create your models here.


class Search(models.Model):
    search_content = models.CharField(max_length=100)
    search_url = models.CharField(max_length=2000)
    search_country = models.CharField(max_length=100, null=True)
    search_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.search_content

    class Meta:
        verbose_name_plural = 'Searches'
