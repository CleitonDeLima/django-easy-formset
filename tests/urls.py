from django.contrib import admin
from django.urls import path

from .testapp import views

urlpatterns = [
    path('formset/', views.formset_view, name='formset'),
    path('modelformset/', views.modelformset_view, name='modelformset'),
    path('admin/', admin.site.urls),
]
