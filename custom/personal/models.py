from random import choices
from tabnanny import verbose
from django.db import models

# # Create your models here.
# PRIRORITY = [('L','Low'), ('M','Medium'), ('H','High')]

# class question(models.Model):
#     title                   = models.CharField(max_length = 60)
#     question                = models.TextField(max_length = 400)
#     priotity                = models.CharField(max_length = 1, choices = PRIRORITY)

#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = "The Question"
#         verbose_name_plural = 'Peoples Questions'