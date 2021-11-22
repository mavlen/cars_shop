from django.contrib import admin
from .models import Cars, CarsImages, Comment
# Register your models here.

class CarsImages(admin.StackedInline):
    model = CarsImages

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    inlines= [CarsImages]

admin.site.register(Comment)