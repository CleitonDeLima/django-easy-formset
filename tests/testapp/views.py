from django import forms
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from easy_formset.forms import NestedInlineFormSet

from tests.forms import AnimalForm, AnimalModelForm, AnimailFormset
from tests.testapp.models import Animal, Home, Person, Address


def formset_view(request):
    formset1 = forms.formset_factory(AnimalForm, extra=0, can_delete=True)(
        prefix="animal1"
    )
    formset2 = forms.formset_factory(
        AnimalForm, extra=1, min_num=1, can_delete=True, max_num=4
    )(prefix="animal2")
    formset3 = forms.formset_factory(AnimalForm, extra=1, min_num=1, can_delete=False)(
        prefix="animal3"
    )

    return render(
        request,
        "formset.html",
        {
            "formset1": formset1,
            "formset2": formset2,
            "formset3": formset3,
        },
    )


def modelformset_view(request):
    animals = Animal.objects.all()
    formset = forms.modelformset_factory(Animal, AnimalModelForm, can_delete=True)
    formset1 = formset(prefix="animal1", queryset=animals)

    return render(request, "modelformset.html", {"formset1": formset1})


def modelformset_view2(request):
    animals = Animal.objects.all()
    formset_class = forms.modelformset_factory(
        Animal, AnimalModelForm, can_delete=True, extra=0
    )

    formset = formset_class(request.POST or None, prefix="animal", queryset=animals)

    if request.method == "POST":
        if formset.is_valid():
            formset.save()

        return redirect("modelformset2")

    return render(request, "modelformset2.html", {"formset": formset})


def formsetevents_view(request):
    formset_class = forms.formset_factory(AnimalForm, extra=1, can_delete=True)
    formset = formset_class(prefix="animal")

    return render(request, "formset_events.html", {"formset": formset})


def nestedmodelformset_view(request):
    animals = Animal.objects.all()
    formset = forms.modelformset_factory(
        Animal, fields=["name", "bio"], formset=AnimailFormset, can_delete=True, extra=0
    )
    f = formset(request.POST or None, prefix="animal", queryset=animals)
    context = {"formset": f}
    if request.method == "POST" and f.is_valid():
        print("save!")
        f.save()
        return redirect("nestedmodelformset")

    return render(request, "nestedmodelformset.html", context)


class PersonFormset(NestedInlineFormSet):
    nested = {
        "addresses": forms.inlineformset_factory(
            Person, Address, fields="__all__", extra=0
        )
    }


class HomeView(DetailView):
    model = Home
    template_name = "nestedinlineformset.html"

    def dispatch(self, request, *args, **kwargs):
        person_formset = forms.inlineformset_factory(
            Home,
            Person,
            formset=PersonFormset,
            fields=["name"],
            extra=0,
        )
        self.formset = person_formset(
            request.POST or None,
            prefix="home",
            queryset=Person.objects.all(),
            instance=self.get_object(),
        )
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj, _ = Home.objects.get_or_create(location="my home")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = self.formset
        return context

    def post(self, request, *args, **kwargs):
        if self.formset.is_valid():
            self.formset.save()
        return redirect("nestedinlineformset")
