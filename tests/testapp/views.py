from django import forms
from django.shortcuts import render

from tests.forms import AnimalForm, AnimalModelForm
from tests.testapp.models import Animal


def formset_view(request):
    formset1 = forms.formset_factory(AnimalForm, extra=0,
                                     can_delete=True)(prefix='animal1')
    formset2 = forms.formset_factory(AnimalForm, extra=1, min_num=1,
                                     can_delete=True, max_num=4)(
        prefix='animal2')
    formset3 = forms.formset_factory(AnimalForm, extra=1, min_num=1,
                                     can_delete=False)(prefix='animal3')

    return render(request, 'formset.html', {
        'formset1': formset1,
        'formset2': formset2,
        'formset3': formset3,
    })


def modelformset_view(request):
    animals = Animal.objects.all()
    formset = forms.modelformset_factory(Animal, AnimalModelForm,
                                         can_delete=True)
    formset1 = formset(prefix='animal1', queryset=animals)

    return render(request, 'modelformset.html', {
        'formset1': formset1
    })
