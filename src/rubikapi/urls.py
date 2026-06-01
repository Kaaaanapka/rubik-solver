from django.urls import path
from .views import solve_endpoint, submit_solve
from .views_export import export_solves_http

urlpatterns = [
    path("solve", solve_endpoint),
    path("submit_solve", submit_solve),

    # eksport TYLKO CSV – obsługujemy obie wersje: ze slashem i bez
    path("solves/export", export_solves_http),
    path("solves/export/", export_solves_http),
]
