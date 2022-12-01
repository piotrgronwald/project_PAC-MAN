from django.db import models

# Create your models here.
class GRA(models.Model):
    gracz = models.CharField(max_length=50, blank=True, null=True)
    wynik = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.graOdczyt()
    def graOdczyt(self):
        return f'Gracz o imieniu {self.gracz} uzyskał wynik: {self.wynik}'

