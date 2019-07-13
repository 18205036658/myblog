from django.contrib import admin

# Register your models here.
from .models import Comment

class PostAdmin(admin.ModelAdmin):
	list_display = ['id','name', 'email', 'url', 'text', 'created_time','post']

admin.site.register(Comment,PostAdmin)