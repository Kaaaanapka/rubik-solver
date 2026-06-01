# rubikapi/views_export.py
import csv
import io
import json
from datetime import datetime
from django.http import HttpResponse
from django.utils.timezone import make_aware, get_default_timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Solve

print("[views_export] loaded")

def _parse_date(s: str):
    return make_aware(datetime.strptime(s, "%Y-%m-%d"), get_default_timezone())

def fmt_time_str(ms: int) -> str:
    if ms is None:
        return ""
    total_ms = int(ms)
    minutes = total_ms // 60000
    seconds = (total_ms % 60000) // 1000
    millis  = total_ms % 1000
    return f"{minutes:02d}:{seconds:02d}.{millis:03d}"

@api_view(["GET"])
@permission_classes([AllowAny])
def export_solves_http(request):
    """
    GET /api/solves/export?method=LBL&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD&with_moves=1
    Zwraca plik CSV z danymi solve’ów.
    """
    method = request.GET.get("method")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    with_moves = request.GET.get("with_moves") in ("1", "true", "True")

    qs = Solve.objects.all().order_by("id")

    if method:
        qs = qs.filter(method=method)

    # sprawdzamy czy model ma created_at
    has_created_at = "created_at" in [f.name for f in Solve._meta.get_fields()]
    if has_created_at:
        if date_from:
            qs = qs.filter(created_at__gte=_parse_date(date_from))
        if date_to:
            dt = _parse_date(date_to).replace(hour=23, minute=59, second=59, microsecond=999999)
            qs = qs.filter(created_at__lte=dt)

    # kolumny w CSV
    cols = ["id", "method", "time_ms", "time_s", "time_str", "length_htm", "length_qtm"]
    if has_created_at:
        cols.append("created_at")
    if hasattr(Solve, "state_54"):
        cols.append("state_54")
    if with_moves:
        cols.append("moves")

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, delimiter=";")
    w.writeheader()

    for s in qs:
        row = {
            "id": s.id,
            "method": getattr(s, "method", None),
            "time_ms": getattr(s, "time_ms", None),
            "length_htm": getattr(s, "length_htm", None),
            "length_qtm": getattr(s, "length_qtm", None),
            "created_at": getattr(s, "created_at", None) if has_created_at else None,
            "state_54": getattr(s, "state_54", None) if hasattr(s, "state_54") else None,
        }
        if with_moves:
            mv = getattr(s, "moves", None)
            if isinstance(mv, (list, tuple)):
                row["moves"] = json.dumps(mv, ensure_ascii=False)
            else:
                row["moves"] = mv
        w.writerow({k: v for k, v in row.items() if k in cols})

    data = buf.getvalue().encode("utf-8")
    resp = HttpResponse(data, content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = 'attachment; filename="solves.csv"'
    return resp
