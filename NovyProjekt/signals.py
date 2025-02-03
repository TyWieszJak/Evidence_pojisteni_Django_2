from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Uzivatel
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate


@receiver(post_save, sender=User)
def Vytvorit_profil_uzivatele(sender, instance, created, **kwargs):
    if created:
        Uzivatel.objects.create(user=instance)


def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Administrators')
    Group.objects.get_or_create(name='Insured')


post_migrate.connect(create_groups)
