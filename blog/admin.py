from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("user", 'get_html_photo', "title",
                    "category", "created_date")
    list_display_links = ("user", 'get_html_photo', "title")
    ordering = ('user', "created_date")
    list_filter = ('user', "category", "tags", 'created_date')
    search_fields = ('user',)
    save_on_top = True
    readonly_fields = ('created_date', 'get_html_photo')

    fieldsets = (
        (None, {
            'fields': (
                ('user',),
            )
        }),
        ("Стаття", {
            'fields': (
                ('title', 'slug'), 'description',
                ('banner', 'get_html_photo')
            )
        }),
        (None, {
            'fields': (
                ('category', 'tags'),
            )
        }),
        ("👍", {
            'fields': (
                ('likes',),
            )
        }),
        ('Дати', {
            'fields': (
                ('created_date',),
            )
        }),
    )

    def get_html_photo(self, object):
        if object.banner:
            return mark_safe(
                f"<img src='{object.banner.url}' width=80>")
        else:
            return "Без фото"

    get_html_photo.short_description = "Мініатюра"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'created_date')
    list_display_links = ('user', 'blog')
    ordering = ('user', 'created_date')
    list_filter = ('user', 'created_date')
    search_fields = ('user',)
    fields = ('user', 'blog', 'text', 'created_date')
    readonly_fields = ('created_date',)


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_date')
    list_display_links = ('user', 'comment')
    ordering = ('user', 'created_date')
    list_filter = ('user', 'created_date')
    search_fields = ('user',)
    readonly_fields = ('created_date',)

    fieldsets = (
        (None, {
            'fields': (
                ('user', 'created_date'),
            )
        }),
        (None, {
            'fields': (
                ('comment', 'text'),
            )
        }),
    )


admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Blog)
# admin.site.register(Comment)
# admin.site.register(Reply)
