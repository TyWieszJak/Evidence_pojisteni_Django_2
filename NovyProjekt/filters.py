import django_filters
from .models import Pojistenec


class PojistenecFilter(django_filters.FilterSet):
    jmeno = django_filters.CharFilter(lookup_expr='icontains', label="Jméno")
    prijmeni = django_filters.CharFilter(lookup_expr='icontains', label="Příjmení")

    # Přidání možnosti pro třídění
    order_by = django_filters.ChoiceFilter(
        choices=[
            ('jmeno', 'Jméno'),
            ('id', 'Datum vytvoření'),
        ],
        label='Seřadit podle',
        method='filter_order_by',  # Metoda pro aplikaci třídění
    )

    class Meta:
        model = Pojistenec
        fields = ['jmeno', 'prijmeni', 'order_by']

    def filter_order_by(self, queryset, name, value):
        if value == 'jmeno':
            return queryset.order_by('jmeno')
        elif value == 'id':
            return queryset.order_by('id')
        return queryset
