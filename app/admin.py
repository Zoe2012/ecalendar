from datetime import date
from django.contrib import admin
from django import forms
from django.contrib.admin import SimpleListFilter
from django.utils.html import escape
from app.models import *

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('date', 'name')
    list_filter = ('date', 'name')
    ordering = ('date',)

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        widgets = {
            'tags':forms.SelectMultiple(attrs={'size': 12})
        }

class OutdatedListFilter(SimpleListFilter):
    title = 'Outdated'
    parameter_name = 'outdated'

    def lookups(self, request, model_admin):
        return (
                ('Yes', 'Yes'),
                ('No', 'No'),
                )
    def queryset(self, request, queryset):
        today = date.today()
        if self.value() == 'Yes':
            return queryset.filter(start_date__lt=today)
        else:
            return queryset.filter(start_date__gte=today)


class ActivityAdmin(admin.ModelAdmin):
    form = ActivityForm
    list_display = ('title', 'abstract', 'location', 'weight', 'status', 'city', 'origin', 'start_date', 'start_time', 'end_date')
    list_display_links = ('abstract',)
    list_editable = ('weight', 'title', 'location')
    list_filter = ('status', 'source', 'tags', OutdatedListFilter, 'start_date', 'end_date', 'city')
    search_fields = ['title', 'content']
    ordering = ('-start_date', '-start_time', '-weight')
    actions = ['make_public', 'make_useless', 'recrawl']

    def make_public(self, request, queryset):
        queryset.update(status=1)
    make_public.short_description = 'Mark selected as public'

    def make_useless(self, request, queryset):
        queryset.update(status=3)
    make_useless.short_description = 'Mark selected as useless'

    def recrawl(self, request, queryset):
        for obj in queryset:
            try:
                starturl = StartURL.objects.get(url=obj.url)
                starturl.status = 's'
                starturl.save()
            except:
                continue
    recrawl.short_description = 'Re crawl selected'

    def abstract(self, obj):
        ans = obj.content[:60]
        if not ans:
            ans = 'Content is empty.'
        else:
            ans = '<a href="' + str(obj.id) + '/" title="' + escape(obj.content) + '">' + escape(ans) + '</a>'
        return ans
    abstract.allow_tags = True

    def origin(self, obj):
        return '<a href="' + obj.url + '" target="_blank">' + obj.source + '</a>'
    origin.allow_tags = True
    

class StartURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'status', 'modified_time', 'crawl_start_time', 'crawl_end_time', 'go')
    list_display_links = ('url', 'modified_time',)
    list_filter = ('status',)
    search_fields = ['url']
    ordering = ('-modified_time',)
    actions = ['make_submitted']

    def make_submitted(self, request, queryset):
        queryset.update(status='s')
    make_submitted.short_description = 'Mark selected URL as submitted status'

    def go(self, obj):
        return '<a href="' + obj.url + '" target="_blank">go</a>'
    go.allow_tags = True


class ReactionAdmin(admin.ModelAdmin):
    list_display = ('activity', 'device', 'like', 'dislike', 'clicked', 'created_time')
    ordering = ('-created_time',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('content', 'device', 'created_time')
    ordering = ('-created_time',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('pinyin', 'name')
    ordering = ('pinyin',)

admin.site.register(Calendar, CalendarAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Tag)
admin.site.register(Device)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Reaction, ReactionAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(StartURL, StartURLAdmin)
admin.site.register(Apk)
admin.site.register(Blacklist)
