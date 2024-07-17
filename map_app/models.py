from django.db import models

# Create your models here.


class HikingTrail(models.Model):
    kml_file_name = models.CharField(max_length=100)
    trail_name = models.CharField(max_length=100)
    distance = models.CharField(max_length=100)
    elevation_gain = models.CharField(max_length=100)
    elevation_loss = models.CharField(max_length=100)
    technical_difficulty = models.CharField(max_length=50)
    max_elevation = models.CharField(max_length=100)
    min_elevation = models.CharField(max_length=100)
    trail_type = models.CharField(max_length=50)
    total_time = models.CharField(max_length=100)
    recorded = models.CharField(max_length=50)
    url = models.URLField(max_length=200)

    class Meta:
        db_table = 'hiking'

    def __str__(self):
        return self.trail_name
