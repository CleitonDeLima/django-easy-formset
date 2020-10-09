from django import forms
from easy_formset.forms import NestedModelFormset
from tests.testapp.models import Animal, Thing, Food


class AnimalForm(forms.Form):
    name = forms.CharField()
    bio = forms.CharField()


class AnimalModelForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ["name", "bio"]


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ["name"]

    def clean_name(self):
        value = self.cleaned_data["name"]
        if len(value) < 2:
            raise forms.ValidationError("error")
        return value

    def clean(self):
        data = super().clean()
        name = data.get("name", "")

        if name == "ahhhh":
            raise forms.ValidationError("ahhhh")

        return data


class ThingFormset(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        names = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            name = form.cleaned_data.get("name")
            if name in names:
                raise forms.ValidationError("Thing in a set must have distinct names.")
            names.append(name)


class AnimailFormset(NestedModelFormset):
    nested = {
        "thing": forms.inlineformset_factory(
            Animal,
            Thing,
            form=ThingForm,
            formset=ThingFormset,
            fields=["name"],
            extra=0,
        ),
        "food": forms.inlineformset_factory(
            Animal,
            Food,
            fields=["name"],
            extra=0,
        ),
    }

    def clean(self):
        if any(self.errors):
            return

        names = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            name = form.cleaned_data.get("name")
            if name in names:
                raise forms.ValidationError(
                    "Animals in a set must have distinct names."
                )
            names.append(name)
