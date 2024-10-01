from django.db import models

class Pojistenec(models.Model):
    jmeno = models.CharField(max_length=100)
    prijmeni = models.CharField(max_length=100)
    adresa = models.CharField(max_length=255)
    vek = models.IntegerField()
    foto = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.jmeno

class Pojisteni(models.Model):
    pojistenec = models.ForeignKey(Pojistenec, on_delete=models.CASCADE, related_name='pojisteni')
    typ_pojisteni = models.CharField(max_length=100)
    datum_sjednani = models.DateField()
    platnost_do = models.DateField()
    castka = models.DecimalField(max_digits=10, decimal_places=2, default=0 )


    def __str__(self):
        return f"{self.typ_pojisteni} - {self.pojistenec}"