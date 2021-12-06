from django.contrib import admin
from .models import Comment, Search

# Register your models here.


admin.site.register(Search)
admin.site.register(Comment)
