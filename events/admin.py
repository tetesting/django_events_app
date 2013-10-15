from django.contrib import admin
from .models import Tag, User, Event


class TagInline(admin.TabularInline):
    model = Tag
    extra = 3

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [TagInline]

    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Event)
