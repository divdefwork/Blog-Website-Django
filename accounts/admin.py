from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('get_html_photo', "username", 'last_login', 'is_active')
    list_display_links = ('get_html_photo', 'username',)
    list_filter = ('username', 'date_joined')
    search_fields = ('username',)
    list_editable = ('is_active',)
    save_on_top = True
    readonly_fields = ('date_joined', 'last_login', 'get_html_photo')
    fieldsets = (
        ('Користувач', {
            'fields': (('username', 'password'),
                       'email',
                       ('first_name', 'last_name'),)
        }),
        ("Дозволи", {
            "fields": ("is_active", ("is_staff", "is_superuser"),
                       "groups", "user_permissions",)
        }),
        (None, {
            'fields': (('profile_image', 'get_html_photo'), 'followers',)
        }),
        ('Важливі дати', {
            'fields': (
                ('date_joined', 'last_login'),)
        }),
    )

    def get_html_photo(self, object):
        if object.profile_image:
            return mark_safe(f"<img src='{object.profile_image.url}' width=50>")
        else:
            return "Без фото"

    get_html_photo.short_description = "Мініатюра"


# admin.site.register(User)
admin.site.register(Follow)
