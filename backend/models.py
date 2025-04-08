from django.db import models

class soil(models.Model):
    moisture=models.FloatField(default=0)
    temperature=models.FloatField(default=0)

class Soildata(models.Model):
    district = models.CharField(max_length=100)
    ph = models.FloatField()
    texture = models.CharField(max_length=50)


# class predict(models.Model):
#     logitude=models.FloatField(defaut=0)
#     latitude=models.FloatField(default=0)
#     ph=models.FloatField(default=0)
#     district=models.CharField(max_length=200)
#     soiltexture=models.CharField(max_length=200)

    
