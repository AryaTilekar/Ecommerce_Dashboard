from django.db import models

class RealtimeData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    source = models.CharField(max_length=255, blank=True)

class HistoricData(models.Model):
    timestamp = models.DateTimeField()
    value = models.FloatField()
    source = models.CharField(max_length=255, blank=True)
