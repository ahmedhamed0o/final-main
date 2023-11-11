from django.contrib import admin
from .models import User, category, articles, comments, role


# Register your models here.
admin.site.register(User)
admin.site.register(category)
admin.site.register(articles)
admin.site.register(comments)
admin.site.register(role)