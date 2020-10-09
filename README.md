# django-easy-formset

Django Formsets with ECMAScript 6

![Python tests](https://github.com/CleitonDeLima/django-easy-formset/workflows/Python%20tests/badge.svg)
![Upload Python Package](https://github.com/CleitonDeLima/django-easy-formset/workflows/Upload%20Python%20Package/badge.svg)

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

## Video
[![Video](https://img.youtube.com/vi/TTXwUOZY_y4/0.jpg)](https://www.youtube.com/watch?v=TTXwUOZY_y4)


## In template
```djangotemplate
{% load static %}
<head>
  <link rel="stylesheet" href="{% static 'easy_formset/easy_formset.css' %}">
</head>
<body>
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
  ...
  <script src="{% static 'easy_formset/easy_formset.js' %}"></script>
  <script>
    const formset = new Formset("{{ formset.prefix }}")
  </script>
</body>
```

## Custom undo element

```js
// add one root element...
Formset.revertHTML = '<a href="#">Custom undo link...</a>'

const formset = new Formset("{{ formset.prefix }}")
```

## Handle add/deleted events

```javascript
document.addEventListener('formset:add', (event) => {
  // access the form with event.detail.form
})

document.addEventListener('formset:deleted', (event) => {
  // access the form with event.detail.form
})
```

## Nested formsets

See examples in `tests.testapp`.


# Run tests
```bash
python -m pip -r requirements.txt
pytest
```

# Run project test
```bash
python manage.py runserver
```
