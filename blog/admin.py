from django.contrib import admin
from .models import Posts, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Posts)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')
    list_filter = ('created_on', 'status')
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(approved=True)