from django.db import models

class soil(models.Model):
    moisture=models.FloatField(default=0)
    temperature=models.FloatField(default=0)
    
