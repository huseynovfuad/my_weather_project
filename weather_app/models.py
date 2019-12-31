from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'