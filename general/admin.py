from django.contrib import admin

# Register your models here.
from general.models import City, MediaFile, ResponseAboutApp, Version
from utils.restrict_view_by_roles import restrict_view_if_not_admin


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return restrict_view_if_not_admin(request)


@admin.register(MediaFile)
class MediaAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return restrict_view_if_not_admin(request)


@admin.register(ResponseAboutApp)
class ResponseAboutAppAdmin(admin.ModelAdmin):
    def users_fullname(self, obj):
        return obj.user.fullname

    def users_number(self, obj):
        return obj.user.phone

    users_fullname.short_description = 'Имя пользователя'
    users_number.short_description = 'Номер телефона'
    readonly_fields = ['users_fullname', 'created_at', 'updated_at']
    list_display = ['user', 'status', 'created_at', 'updated_at']
    list_filter = ['status']

    def get_model_perms(self, request):
        return restrict_view_if_not_admin(request)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['type', 'version', 'hard']

    def get_model_perms(self, request):
        return restrict_view_if_not_admin(request)

class MediaFilesInlineAdmin(admin.TabularInline):
    model = MediaFile
