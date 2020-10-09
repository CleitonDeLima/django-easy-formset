from django.contrib import admin

from .models import Animal, Thing, Food, Home, Person, Address


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    class ThingInline(admin.TabularInline):
        extra = 0
        model = Thing

    class FoodInline(admin.TabularInline):
        extra = 0
        model = Food

    inlines = [ThingInline, FoodInline]


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    class PersonInline(admin.TabularInline):
        extra = 0
        model = Person

    inlines = [PersonInline]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    class AddressInline(admin.TabularInline):
        model = Address

    inlines = [AddressInline]
