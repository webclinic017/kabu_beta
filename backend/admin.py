from django.contrib import admin
from backend.model.company import COMPANY
from backend.model.wordmask import wordMask

# Register your models here.
admin.site.register(COMPANY)
admin.site.register(wordMask)