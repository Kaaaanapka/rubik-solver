from django.contrib import admin
from .models import Solve

@admin.register(Solve)
class SolveAdmin(admin.ModelAdmin):
    list_display = ("id", "method", "time_ms", "length_htm", "length_qtm", "created_at")
    list_filter = ("method", "created_at")
    search_fields = ("method",)