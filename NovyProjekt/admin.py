from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import PojistnaUdalost

# Vytvořte skupiny a přiřaďte jim oprávnění
admin_group, created = Group.objects.get_or_create(name='Administrators')
insured_group, created = Group.objects.get_or_create(name='Insured')

# Přiřazení oprávnění pro administrátora
admin_permissions = Permission.objects.all()
admin_group.permissions.set(admin_permissions)

# Přiřazení omezených oprávnění pro pojištěného
content_type = ContentType.objects.get_for_model(PojistnaUdalost)
insured_permissions = Permission.objects.filter(content_type=content_type)
insured_group.permissions.set(insured_permissions)