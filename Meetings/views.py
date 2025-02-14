from django.shortcuts import redirect
from django.views.generic import CreateView
from .models import Schuzka
from NovyProjekt.models import Uzivatel
from django.urls import reverse_lazy
from .services import SchuzkaService
from django.http import Http404

class SchuzkaCreateView(CreateView):
    model = Schuzka
    fields = ['datum_cas', 'poznamka']
    template_name = 'schuzky/schuzka_kalendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            pojistenec = Uzivatel.objects.get(pk=self.kwargs['pk'])
            context['pojistenec'] = pojistenec
        except Uzivatel.DoesNotExist:
            raise Http404("Pojištěnec nenalezen.")
        return context

    def form_valid(self, form):
        """Pokud je formulář validní, zjistíme, zda už pojištěnec má schůzku. Pokud ano, přepíšeme ji."""
        pojistenec = Uzivatel.objects.get(pk=self.kwargs['pk'])
        schuzka = Schuzka.objects.filter(pojistenec=pojistenec).first()

        if schuzka:
            schuzka.datum_cas = form.cleaned_data['datum_cas']
            schuzka.poznamka = form.cleaned_data['poznamka']
            schuzka.save()
        else:
            form.instance.pojistenec = pojistenec
            form.save()

        return redirect('detail_pojistence', pk=pojistenec.pk)
