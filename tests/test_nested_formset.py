from django import forms

from tests.testapp.models import Animal, Thing, Food
from tests.forms import AnimailFormset


class TestNestedModelFormset:
    def test_formset_is_valid(self, db):
        formset = forms.modelformset_factory(
            Animal, formset=AnimailFormset, fields=["name"]
        )
        data = {
            "animal-TOTAL_FORMS": "2",
            "animal-INITIAL_FORMS": "0",
            "animal-MIN_NUM_FORMS": "0",
            "animal-MAX_NUM_FORMS": "1000",
            "animal-0-name": "Gato",
            "animal-0-bio": "Gatinhooooo",
            "animal-0-id": "",
            "animal-0-thing-TOTAL_FORMS": "3",
            "animal-0-thing-INITIAL_FORMS": "0",
            "animal-0-thing-MIN_NUM_FORMS": "0",
            "animal-0-thing-MAX_NUM_FORMS": "1000",
            "animal-0-thing-0-name": "thing1",
            "animal-0-thing-0-id": "",
            "animal-0-thing-1-name": "thing2",
            "animal-0-thing-1-id": "",
            "animal-0-thing-2-name": "thing3",
            "animal-0-thing-2-id": "",
            "animal-0-food-TOTAL_FORMS": "1",
            "animal-0-food-INITIAL_FORMS": "0",
            "animal-0-food-MIN_NUM_FORMS": "0",
            "animal-0-food-MAX_NUM_FORMS": "1000",
            "animal-0-food-0-name": "egg",
            "animal-0-food-0-id": "",
            "animal-1-name": "Cachorro",
            "animal-1-bio": "dog dog",
            "animal-1-id": "",
            "animal-1-thing-TOTAL_FORMS": "2",
            "animal-1-thing-INITIAL_FORMS": "0",
            "animal-1-thing-MIN_NUM_FORMS": "0",
            "animal-1-thing-MAX_NUM_FORMS": "1000",
            "animal-1-thing-0-name": "thing1",
            "animal-1-thing-0-id": "",
            "animal-1-thing-1-name": "thing2",
            "animal-1-thing-1-id": "",
            "animal-1-food-TOTAL_FORMS": "0",
            "animal-1-food-INITIAL_FORMS": "0",
            "animal-1-food-MIN_NUM_FORMS": "0",
            "animal-1-food-MAX_NUM_FORMS": "1000",
        }
        f = formset(data, prefix="animal")
        assert f.is_valid()
        f.save()
        assert Animal.objects.count() == 2
        assert Thing.objects.count() == 5
        assert Food.objects.count() == 1
        animal1 = Animal.objects.first()
        animal2 = Animal.objects.last()
        assert animal1.thing_set.count() == 3
        assert animal1.food_set.count() == 1
        assert animal2.thing_set.count() == 2

    def test_nested_form_field_error(self, db):
        formset = forms.modelformset_factory(
            Animal, formset=AnimailFormset, fields=["name"]
        )
        data = {
            "animal-TOTAL_FORMS": "1",
            "animal-INITIAL_FORMS": "0",
            "animal-MIN_NUM_FORMS": "0",
            "animal-MAX_NUM_FORMS": "1000",
            "animal-0-name": "Gato",
            "animal-0-bio": "Gatinhooooo",
            "animal-0-id": "",
            "animal-0-thing-TOTAL_FORMS": "1",
            "animal-0-thing-INITIAL_FORMS": "0",
            "animal-0-thing-MIN_NUM_FORMS": "0",
            "animal-0-thing-MAX_NUM_FORMS": "1000",
            "animal-0-thing-0-name": "a",
            "animal-0-thing-0-id": "",
            "animal-0-food-TOTAL_FORMS": "0",
            "animal-0-food-INITIAL_FORMS": "0",
            "animal-0-food-MIN_NUM_FORMS": "0",
            "animal-0-food-MAX_NUM_FORMS": "1000",
        }
        f = formset(data, prefix="animal")
        assert not f.is_valid()
        assert list(f.forms[0].thing.errors) == [{"name": ["error"]}]

    def test_nested_form_non_error(self, db):
        formset = forms.modelformset_factory(
            Animal, formset=AnimailFormset, fields=["name"]
        )
        data = {
            "animal-TOTAL_FORMS": "1",
            "animal-INITIAL_FORMS": "0",
            "animal-MIN_NUM_FORMS": "0",
            "animal-MAX_NUM_FORMS": "1000",
            "animal-0-name": "Gato",
            "animal-0-bio": "Gatinhooooo",
            "animal-0-id": "",
            "animal-0-thing-TOTAL_FORMS": "1",
            "animal-0-thing-INITIAL_FORMS": "0",
            "animal-0-thing-MIN_NUM_FORMS": "0",
            "animal-0-thing-MAX_NUM_FORMS": "1000",
            "animal-0-thing-0-name": "ahhhh",
            "animal-0-thing-0-id": "",
        }
        f = formset(data, prefix="animal")
        assert not f.is_valid()
        assert list(f.forms[0].thing.errors) == [{"__all__": ["ahhhh"]}]

    def test_non_formset_error(self, db):
        formset = forms.modelformset_factory(
            Animal, formset=AnimailFormset, fields=["name"]
        )
        data = {
            "animal-TOTAL_FORMS": "2",
            "animal-INITIAL_FORMS": "0",
            "animal-MIN_NUM_FORMS": "0",
            "animal-MAX_NUM_FORMS": "1000",
            "animal-0-name": "Gato",
            "animal-0-bio": "Gatinhooooo",
            "animal-0-id": "",
            "animal-1-name": "Gato",
            "animal-1-bio": "cat cat",
            "animal-1-id": "",
            "animal-0-thing-TOTAL_FORMS": "0",
            "animal-0-thing-INITIAL_FORMS": "0",
            "animal-0-thing-MIN_NUM_FORMS": "0",
            "animal-0-thing-MAX_NUM_FORMS": "1000",
            "animal-1-thing-TOTAL_FORMS": "0",
            "animal-1-thing-INITIAL_FORMS": "0",
            "animal-1-thing-MIN_NUM_FORMS": "0",
            "animal-1-thing-MAX_NUM_FORMS": "1000",
        }
        f = formset(data, prefix="animal")
        assert not f.is_valid()
        assert f.non_form_errors() == ["Animals in a set must have distinct names."]

    def test_nested_non_formset_error(self, db):
        formset = forms.modelformset_factory(
            Animal, formset=AnimailFormset, fields=["name"]
        )
        data = {
            "animal-TOTAL_FORMS": "1",
            "animal-INITIAL_FORMS": "0",
            "animal-MIN_NUM_FORMS": "0",
            "animal-MAX_NUM_FORMS": "1000",
            "animal-0-name": "Gato",
            "animal-0-bio": "cat",
            "animal-0-id": "",
            "animal-0-thing-TOTAL_FORMS": "2",
            "animal-0-thing-INITIAL_FORMS": "0",
            "animal-0-thing-MIN_NUM_FORMS": "0",
            "animal-0-thing-MAX_NUM_FORMS": "1000",
            "animal-0-thing-0-name": "thing1",
            "animal-0-thing-0-id": "",
            "animal-0-thing-1-name": "thing1",
            "animal-0-thing-1-id": "",
        }
        f = formset(data, prefix="animal")
        assert not f.is_valid()
        assert f.forms[0].thing.non_form_errors() == [
            "Thing in a set must have distinct names."
        ]
