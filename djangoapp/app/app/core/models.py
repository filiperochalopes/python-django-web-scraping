from django.db import models

class Tag(models.Model):
    name = models.TextField(max_length=100, unique=True)
    description_pt_br = models.TextField(blank=True)
    description_en_us = models.TextField(blank=True)
    color_hex = models.TextField(max_length=6, default='cccccc')
    parent = models.ForeignKey('Tag', on_delete=models.CASCADE, blank=True, null=True)
