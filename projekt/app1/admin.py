from django.contrib import admin
from .models import Uloga, Predmet, Korisnik, Upis
from django.contrib.auth.admin import UserAdmin

admin.site.register(Uloga)
admin.site.register(Predmet)
admin.site.register(Upis)


@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('uloga', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('uloga', 'status')}),
    )

    list_display = ('username', 'email', 'uloga', 'status', 'is_staff')
