from django.contrib import admin
from .models import Note, Category

# Register your models here.
admin.site.register(Note)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Category, CategoryAdmin)
