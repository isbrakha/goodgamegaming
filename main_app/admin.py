from django.contrib import admin
from .models import UserProfile, Game, Tip, Review

# Register your models here.
admin.site.register(Game)
admin.site.register(Tip)
admin.site.register(Review)
admin.site.register(UserProfile)