from django.contrib import admin
from .models import Category, Blog


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    # category__category_name this field is foreign key so two model field names are required for 
    # searching
    list_editable = ('is_featured',)


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
