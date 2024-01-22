from django.contrib import admin
from .models import User, Game, Tip, Review

# Register your models here.
admin.site.register(Game)
admin.site.register(Tip)
admin.site.register(Review)