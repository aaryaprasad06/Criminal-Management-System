from django.contrib import admin
from .models import Criminal, Crime, Arrest, CaseFile

admin.site.register(Criminal)
admin.site.register(Crime)
admin.site.register(Arrest)
admin.site.register(CaseFile)