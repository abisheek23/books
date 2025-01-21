from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(locations)
admin.site.register(Category)
admin.site.register(genres)
admin.site.register(books)
admin.site.register(Borrow)
admin.site.register(Contact)
