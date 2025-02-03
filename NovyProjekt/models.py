from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone


# Vlastní správa uživatelů
class UzivatelManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Uživatel musí mít emailovou adresu.")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


# Vlastní model uživatele
class Uzivatel(AbstractBaseUser):
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=300, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)
    foto = models.ImageField(upload_to='images/', blank=True, null=True)

    objects = UzivatelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


# Model Pojistenec
class Pojistenec(models.Model):
    user = models.ForeignKey(Uzivatel, on_delete=models.CASCADE,
                             null=True, blank=True)
    jmeno = models.CharField(max_length=100)
    prijmeni = models.CharField(max_length=100)
    adresa = models.CharField(max_length=255)
    vek = models.IntegerField(null=True)
    foto = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"


# Model Pojisteni
class Pojisteni(models.Model):
    POJISTENI_CHOICES = [
        ('majetek', 'Pojištění majetku'),
        ('zivotni', 'Životní pojištění'),
        ('cestovni', 'Cestovní pojištění'),
        ('vozidla', 'Pojištění vozidel'),
        ('zdravotni', 'Zdravotní pojištění'),
        ('urazove', 'Úrazové pojištění'),
        ('odpovednost', 'Pojištění odpovědnosti'),
        ('domacnost', 'Pojištění domácnosti'),
        ('pravni_ochrana', 'Pojištění právní ochrany'),
        ('podnikani', 'Pojištění podnikatelských rizik'),
    ]

    pojistenec = models.ForeignKey(Pojistenec, on_delete=models.CASCADE,
                                   related_name='pojisteni')
    typ_pojisteni = models.CharField(max_length=50, choices=POJISTENI_CHOICES)
    predmet_pojisteni = models.CharField(max_length=100)
    datum_sjednani = models.DateField()
    platnost_do = models.DateField()
    castka = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f" {self.pojistenec}"


# Model PojistnaUdalost
class PojistnaUdalost(models.Model):
    STATUS_CHOICES = [
        ('nahlaseno', 'Nahlášeno'),
        ('vyreseno', 'Vyřešeno'),
        ('ceka_na_schvaleni', 'Čeká na schválení'),
    ]

    pojisteni = models.ForeignKey(Pojisteni, on_delete=models.CASCADE,
                                  related_name='udalosti')
    datum_udalosti = models.DateField()
    popis = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    castka = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        pojisteni_text = str(self.pojisteni) if self.pojisteni else "Neznámé pojištění"
        return f"Událost: {pojisteni_text} - Status: {self.status}"
