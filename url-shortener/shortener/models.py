from django.db import models
import random, string



class UrlData(models.Model):
    url = models.URLField(max_length=500)
    slug = models.SlugField(max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    #count = models.IntegerField(default=0)

    def generate_slug(self, length=7):
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(chars) for _ in range(length))
            if not UrlData.objects.filter(slug=code).exists():
                return code#

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

#total = UrlData.objects.count()
class GlobalCounter(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.IntegerField(default=0)