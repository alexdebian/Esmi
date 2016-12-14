from django.contrib import admin
from django.contrib.auth.models import Group
from esmiapp.models import *
from esmiapp.models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'middle_name', 'birthday', 'phonenumber', 'email']
    list_display_links = ['username', 'email', 'first_name', 'last_name', 'middle_name', 'birthday', 'phonenumber', ]
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'gender')
        }),
        ('Дополнительные параметры', {
            'classes': ('collapse',),
            'fields': ('middle_name', 'phonenumber', 'birthday')
        }),
        ('Адрес', {
            'classes': ('collapse',),
            'fields': ('country', 'index', 'city', 'street', 'house', 'apartment')
        }),
    )
admin.site.register(Users, UsersAdmin)
admin.site.unregister(Group)


@admin.register(EsmiIsLikedIssue)
class AdminIsLiked(admin.ModelAdmin):
    list_display = ['iduser', 'idissue']
    list_display_links = ['iduser', 'idissue']


@admin.register(EsmiIsPayedIssue)
class AdminIsLiked(admin.ModelAdmin):
    list_display = ['iduser', 'idissue']
    list_display_links = ['iduser', 'idissue']


@admin.register(EsmiNews)
class AdminEsmiNews(admin.ModelAdmin):
    list_display = ['id', 'header', 'data_publication']
    list_display_links = ['header']
    list_filter = ['idindexlevel2']

    fieldsets = (
        ('Основное', {
            'classes': ('collapse',),
            'fields': ('newstype', 'typeartical', 'idindexlevel2', 'header', 'data_create'),
        }),
        ('Meta', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'meta_tags'),
        }),
        ('Картинка', {
            'classes': ('collapse',),
            'fields': ('picture', 'pct_description', 'alt'),
        }),
        ('Материал', {
            'classes': ('collapse',),
            'fields': ('description', 'body_free', 'body_close'),
        }),
        ('Подвал', {
            'classes': ('collapse',),
            'fields': ('idauthor', 'idissue', 'data_publication', 'tags'),
        })
    )


@admin.register(EsmiIndexLevel1)
class AdminEsmiIndexLevel1(admin.ModelAdmin):
    fieldsets = [('Rubricator', {'fields': ['indexlevel1']})]
    list_display = ['indexlevel1']
    list_display_links = ['indexlevel1']


@admin.register(EsmiIndexLevel2)
class AdminEsmiIndexLevel2(admin.ModelAdmin):
    list_display = ['indexlevel2ru']
    list_display_links = ['indexlevel2ru']


@admin.register(EsmiAuthors)
class AdminEsmiAuthors(admin.ModelAdmin):
    list_display = ['author']
    list_display_links = ['author']


@admin.register(EsmiIssues)
class AdminEsmiIssues(admin.ModelAdmin):
    list_display = ['__str__', 'idnameedition']
    list_display_links = ['__str__']
    list_filter = ['idnameedition']


@admin.register(EsmiEditionNames)
class AdminEsmiEditionNames(admin.ModelAdmin):
    exclude = ['editionname_url']
    list_display = ['editionname_ru']


@admin.register(EsmiEditionTypes)
class AdminEsmiEditionTypes(admin.ModelAdmin):
    list_display = ['editiontype_ru']
    list_display_links = ['editiontype_ru']


@admin.register(EsmiTags)
class AdminEsmiTags(admin.ModelAdmin):
    list_display = ['tag']
    exclude = ['tag_url']


@admin.register(EsmiPublishers)
class AdminEsmiPublishers(admin.ModelAdmin):
    list_display = ['publisher']


@admin.register(EsmiIssueprices)
class AdminEsmiIssueprices(admin.ModelAdmin):
    list_display = ['__str__', 'price']


@admin.register(EsmiNewsTypes)
class AdminEsmiNewsTypes(admin.ModelAdmin):
    list_display = ['newstype']
