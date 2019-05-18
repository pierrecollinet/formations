from django.contrib import admin

from partenaires.models import SalleCours, SalleCoursImage

class SalleCoursImageInline(admin.TabularInline):
    model = SalleCoursImage
    extra = 0
    max_num = 15


class SalleCoursAdmin(admin.ModelAdmin):
    inlines = [
        SalleCoursImageInline,
    ]
    list_display = ['nom',]

    class Meta:
        model = SalleCours

admin.site.register(SalleCours, SalleCoursAdmin)
