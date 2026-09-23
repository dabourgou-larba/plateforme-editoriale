from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Role, Utilisateur, Categorie, Depeche, Media,
    Historique, Client, Abonnement, Diffusion,
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("nom",)


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ("username", "get_full_name", "role", "is_active")
    list_filter = ("role", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Rôle éditorial", {"fields": ("role", "telephone", "localisation")}),
    )


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom",)


class MediaInline(admin.TabularInline):
    model = Media
    extra = 0


class HistoriqueInline(admin.TabularInline):
    model = Historique
    extra = 0
    readonly_fields = ("action", "utilisateur", "date")
    can_delete = False


@admin.register(Depeche)
class DepecheAdmin(admin.ModelAdmin):
    list_display = ("titre", "categorie", "auteur", "statut", "date_creation")
    list_filter = ("statut", "categorie")
    search_fields = ("titre", "contenu")
    inlines = [MediaInline, HistoriqueInline]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nom", "type", "contact_email")


@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ("client", "type_abonnement", "date_debut", "date_fin", "actif")
    list_filter = ("type_abonnement", "actif")


@admin.register(Diffusion)
class DiffusionAdmin(admin.ModelAdmin):
    list_display = ("depeche", "canal", "date_diffusion")
