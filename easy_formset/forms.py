from django.forms import BaseModelFormSet, BaseInlineFormSet


class NestedFormsetMixin:
    nested = {}

    def add_fields(self, form, index):
        super().add_fields(form, index)

        for formset_name, formset in self.nested.items():

            prefix = "{0}-{1}".format(form.prefix, formset_name)
            formset_kwargs = {
                "instance": form.instance,
                "data": form.data if form.is_bound else None,
                "files": form.files if form.is_bound else None,
                "prefix": prefix,
            }
            extra_kwargs_func = getattr(self, f"get_{formset_name}_kwargs", None)
            if callable(extra_kwargs_func):
                extra_kwargs = extra_kwargs_func()
            else:
                extra_kwargs = {}

            formset_kwargs.update(**extra_kwargs)
            setattr(form, formset_name, formset(**formset_kwargs))

    def is_valid(self):
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                for name in self.nested_names:
                    if hasattr(form, name):
                        result = result and getattr(form, name).is_valid()

        return result

    def save(self, commit=True):
        result = super().save(commit=commit)

        for form in self.forms:
            for name in self.nested_names:
                if hasattr(form, name):
                    if not self._should_delete_form(form):
                        getattr(form, name).save(commit=commit)

        return result

    @property
    def nested_names(self):
        return self.nested.keys()

    @property
    def media(self):
        return self.empty_form.media + self.empty_form.nested.media


class NestedModelFormset(NestedFormsetMixin, BaseModelFormSet):
    ...


class NestedInlineFormSet(NestedFormsetMixin, BaseInlineFormSet):
    ...
