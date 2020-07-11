# django-easy-formset

Django Formsets with ECMAScript 6

# Installation

Installation is easy using pip and the only requirement is a recent version of Django.

```bash
python -m pip install django-easy-formset
```

## Basic app configuration
Then to add the Django Easy Formset to your project add the app `easy_formset` to 
your `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    # ...
    "easy_formset",
]
```

# How to use

```djangotemplate
{% load static %}
...
<div id="{{ formset.prefix }}">
  {{ formset.management_form }}

  <template formset-empty-form>
    {{ formset.empty_form.as_p }}
    <a formset-form-delete>Delete</a>
  </template>

  <div formset-forms>
    {% for form in formset.forms %}
      <div formset-form>
        {{ form.as_p }}
        <a formset-form-delete>Delete</a>
      </div>
    {% endfor %}
  </div>

  <button formset-add>Add Formset</button>
</div>

<script src="{% static 'easy_formset/easy_formset.js' %}"></script>
<script>
  const formset = new Formset("{{ formset.prefix }}")
</script>
...
```

# Run tests
```bash
python -m pip -r requirements.txt
pytest
```

# Run project test
```bash
python manage.py runserver
```
