from django.contrib import admin

from .models import Municipality, Position, PublicBody, PublicOfficial

admin.site.site_header = "MyMuniBase"
admin.site.site_title = "MyMuniBase"
admin.site.index_title = "Gestão de municípios clientes"


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ["name", "state", "ibge_code"]
    list_filter = ["state"]
    search_fields = ["name", "ibge_code"]


@admin.register(PublicBody)
class PublicBodyAdmin(admin.ModelAdmin):
    list_display = ["name", "acronym", "kind", "municipality"]
    list_filter = ["kind", "municipality__state"]
    search_fields = ["name", "acronym", "municipality__name"]
    autocomplete_fields = ["municipality"]
    list_select_related = ["municipality"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(PublicOfficial)
class PublicOfficialAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "public_body", "is_active"]
    list_filter = ["is_active", "public_body__kind", "public_body__municipality__state"]
    search_fields = ["name", "email", "public_body__name", "position__name"]
    autocomplete_fields = ["public_body", "position"]
    list_select_related = ["position", "public_body__municipality"]
