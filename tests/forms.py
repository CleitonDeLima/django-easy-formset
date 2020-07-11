from django import forms

from tests.testapp.models import Animal


class AnimalForm(forms.Form):
    name = forms.CharField()
    bio = forms.CharField()


class AnimalModelForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'bio']
