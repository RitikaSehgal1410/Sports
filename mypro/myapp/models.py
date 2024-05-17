from django.db import models

class CSVData(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    credit_score = models.IntegerField()
    credit_lines = models.IntegerField()
    masked_phone_number = models.CharField(max_length=20)