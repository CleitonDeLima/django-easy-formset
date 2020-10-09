from django.contrib import admin
from django.urls import path

from .testapp import views

urlpatterns = [
    path("formset/", views.formset_view, name="formset"),
    path("modelformset/", views.modelformset_view, name="modelformset"),
    path("modelformset2/", views.modelformset_view2, name="modelformset2"),
    path("formset-events/", views.formsetevents_view, name="formset-events"),
    path(
        "nestedmodelformset/", views.nestedmodelformset_view, name="nestedmodelformset"
    ),
    path("nestedinlineformset/", views.HomeView.as_view(), name="nestedinlineformset"),
    path("admin/", admin.site.urls),
]
