from django.contrib import admin
from roojoomSolver.models import Issue


class ReadOnly(admin.ModelAdmin):
     readonly_fields = ('created_at',)

admin.site.register(Issue, ReadOnly)