from django.db import models
from django.contrib.auth.models import User

class Pojistenec(models.Model):
    jmeno = models.CharField(max_length=100)
    prijmeni = models.CharField(max_length=100)
    adresa = models.CharField(max_length=255)
    vek = models.IntegerField()
    foto = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.jmeno

class Pojisteni(models.Model):
    POJISTENI_CHOICES = [
        ('majetek', 'Pojištění majetku (např. dům, byt)'),
        ('zivotni', 'Životní pojištění'),
        ('cestovni', 'Cestovní pojištění'),
        ('vozidla', 'Pojištění vozidel (povinné ručení, havarijní pojištění)'),
        ('zdravotni', 'Zdravotní pojištění'),
        ('urazove', 'Úrazové pojištění'),
        ('odpovednost', 'Pojištění odpovědnosti (škoda způsobená třetí osobě)'),
        ('domacnost', 'Pojištění domácnosti'),
        ('pravni_ochrana', 'Pojištění právní ochrany'),
        ('podnikani', 'Pojištění podnikatelských rizik'),
    ]

    pojistenec = models.ForeignKey(Pojistenec, on_delete=models.CASCADE, related_name='pojisteni')
    typ_pojisteni = models.CharField(max_length=100, choices=POJISTENI_CHOICES)
    predmet_pojisteni = models.CharField(max_length=100, default=None)
    datum_sjednani = models.DateField()
    platnost_do = models.DateField()
    castka = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.get_typ_pojisteni_display()} - {self.pojistenec}"




class PojistnaUdalost(models.Model):
    pojisteni = models.ForeignKey(Pojisteni, on_delete=models.CASCADE, related_name='pojistne_udalosti')
    datum_udalosti = models.DateField()
    popis = models.TextField()

    STATUS_CHOICES = [
            ('nahlášeno', 'Nahlášeno'),
            ('vyřešeno', 'Vyřešeno'),
            ('čeká na schválení', 'Čeká na schválení'),
        ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    castka = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Událost: {self.pojisteni}, Datum: {self.datum_udalosti}, Status: {self.status}"

class Uzivatel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username