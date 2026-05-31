from django.db import models

class Solve(models.Model):
    method = models.CharField(max_length=50, null=True, blank=True)
    time_ms = models.IntegerField(null=True, blank=True)
    moves = models.TextField(null=True, blank=True)
    length_htm = models.IntegerField(null=True, blank=True)
    length_qtm = models.IntegerField(null=True, blank=True)

    #zapisujemy 54-znakowy facelet string
    state_54 = models.CharField(max_length=54, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
