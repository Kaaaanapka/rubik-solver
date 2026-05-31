import csv
import json
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware, get_default_timezone

from rubikapi.models import Solve

class Command(BaseCommand):
    help = "Exportuje rekordy Solve do CSV lub XLSX z opcjonalnymi filtrami."

    def add_arguments(self, parser):
        parser.add_argument("--outfile", required=True, help="Ścieżka do pliku wyjściowego (np. data/solves.csv)")
        parser.add_argument("--format", choices=["csv", "xlsx"], default="csv", help="Format pliku wyjściowego")
        parser.add_argument("--method", help="Filtr: nazwa metody (np. LBL)")
        parser.add_argument("--date-from", help="Filtr: od daty (YYYY-MM-DD)")
        parser.add_argument("--date-to", help="Filtr: do daty (YYYY-MM-DD)")
        parser.add_argument("--with-moves", action="store_true", help="Dołącz kolumnę z ruchami (JSON)")
        parser.add_argument("--delimiter", default=";", help="Separator CSV (domyślnie ';')")

    def handle(self, *args, **opts):
        outfile = Path(opts["outfile"])
        outfmt = opts["format"]
        method = opts.get("method")
        date_from = opts.get("date_from")
        date_to = opts.get("date_to")
        with_moves = bool(opts.get("with_moves"))
        delimiter = opts["delimiter"]

        qs = Solve.objects.all().order_by("id")

        # Filtry
        if method:
            qs = qs.filter(method=method)

        # Filtry dat: próbujemy użyć pola created_at jeśli istnieje; w innym razie pomijamy
        has_created_at = hasattr(Solve, "created_at") or ("created_at" in [f.name for f in Solve._meta.get_fields()])
        tz = get_default_timezone()

        def parse_date(d):
            # YYYY-MM-DD -> aware datetime na północ tej daty
            dt = datetime.strptime(d, "%Y-%m-%d")
            return make_aware(dt, tz)

        if has_created_at:
            if date_from:
                qs = qs.filter(created_at__gte=parse_date(date_from))
            if date_to:
                # do końca dnia
                dt = parse_date(date_to).replace(hour=23, minute=59, second=59, microsecond=999999)
                qs = qs.filter(created_at__lte=dt)
        elif date_from or date_to:
            self.stdout.write(self.style.WARNING("Uwaga: model Solve nie ma pola 'created_at' — filtry dat pominięte."))

        rows = []
        # Ustal kolumny
        base_cols = ["id", "method", "time_ms", "length_htm", "length_qtm"]
        if has_created_at:
            base_cols.append("created_at")
        base_cols.append("state_54") if hasattr(Solve, "state_54") else None
        if with_moves:
            base_cols.append("moves")

        # Zbuduj wynik
        for s in qs:
            row = {
                "id": s.id,
                "method": getattr(s, "method", None),
                "time_ms": getattr(s, "time_ms", None),
                "length_htm": getattr(s, "length_htm", None),
                "length_qtm": getattr(s, "length_qtm", None),
            }
            if has_created_at:
                row["created_at"] = getattr(s, "created_at", None)
            if hasattr(s, "state_54"):
                row["state_54"] = getattr(s, "state_54", None)
            if with_moves:
                # moves w bazie jako tekst/json – spróbujmy normalizować
                mv = getattr(s, "moves", None)
                if isinstance(mv, (list, tuple)):
                    row["moves"] = json.dumps(mv, ensure_ascii=False)
                else:
                    row["moves"] = mv  # może już być JSON string
            rows.append(row)

        outfile.parent.mkdir(parents=True, exist_ok=True)

        if outfmt == "csv":
            with outfile.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, fieldnames=[c for c in base_cols if c], delimiter=delimiter)
                w.writeheader()
                for r in rows:
                    w.writerow(r)
        else:
            # xlsx
            try:
                from openpyxl import Workbook
            except ImportError as e:
                raise CommandError("Brak pakietu 'openpyxl'. Zainstaluj: pip install openpyxl") from e
            wb = Workbook()
            ws = wb.active
            headers = [c for c in base_cols if c]
            ws.append(headers)
            for r in rows:
                ws.append([r.get(c) for c in headers])
            wb.save(str(outfile))

        self.stdout.write(self.style.SUCCESS(f"Zapisano {len(rows)} rekordów -> {outfile}"))
