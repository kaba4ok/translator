# encoding: utf-8

from django.contrib import admin

from translator.translator import models


class LanguagesFromToAdmin(admin.ModelAdmin):
    list_display = (u'html_option',)


class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('languages', 'word', 'translation')
    list_per_page = 500
    ordering = ('languages', 'word')
    list_filter = ('languages',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['langs'] = models.LanguagesFromTo.objects.order_by('id')
        return super(DictionaryAdmin,
                     self).changelist_view(request, extra_context=extra_context)


class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('time_fmt', 'text')
    ordering = ('-time',)
    list_per_page = 500
    fields = ('text',)
    readonly_fields = ('text',)

    def time_fmt(self, obj):
        return obj.time.strftime('%Y-%m-%d %H:%M:%S')

    time_fmt.short_description = u'Время запроса'
    time_fmt.admin_order_field = 'time'

    def has_add_permission(self, obj=None):
        return False


class WordNotFoundAdmin(admin.ModelAdmin):
    list_display = (u'word',)
    fields = ('word',)
    readonly_fields = ('word',)
    list_per_page = 500

    def has_add_permission(self, obj=None):
        return False


site = admin.sites.AdminSite()
site.register(models.LanguagesFromTo, LanguagesFromToAdmin)
site.register(models.Dictionary, DictionaryAdmin)
site.register(models.QueryLog, QueryLogAdmin)
site.register(models.WordNotFound, WordNotFoundAdmin)
