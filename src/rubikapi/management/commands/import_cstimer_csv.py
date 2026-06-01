import csv
import json
import re
from pathlib import Path
from typing import Optional, List, Tuple, Dict

from django.core.management.base import BaseCommand, CommandError
from rubikapi.models import Solve

# ---- Pomocnicze: parsowanie czasu z cstimer ----
# obsługa: "12.34" (sekundy), "1:23.45" (minuty:sekundy), "DNF", "+2"
TIME_RE = re.compile(r"^\s*(?P<min>\d+):(?P<sec>\d+(?:\.\d+)?)\s*$")

def parse_time_to_ms(value: Optional[str], penalty: Optional[str] = None) -> Optional[int]:
    """
    Zwraca milisekundy albo None (jeśli DNF/puste).
    value: np. "12.34" albo "1:23.45" albo "DNF"
    penalty: np. "+2" / "" / None
    """
    if value is None:
        return None
    s = str(value).strip().upper()
    if not s or s == "DNF":
        return None

    # wykryj +2 wewnątrz pola czasu, np. "12.34 (+2)" lub "12.34+2"
    has_p2 = False
    if "+2" in s:
        has_p2 = True
        s = s.replace("+2", "").replace("(+2)", "").strip()

    # "mm:ss.xx"
    m = TIME_RE.match(s)
    if m:
        minutes = int(m.group("min"))
        seconds = float(m.group("sec"))
        base_ms = int(round((minutes * 60 + seconds) * 1000))
    else:
        # tylko sekundy "12.34"
        try:
            base_ms = int(round(float(s) * 1000))
        except ValueError:
            return None

    # pole penalty z CSV (np. oddzielna kolumna)
    if penalty:
        pen = str(penalty).strip()
        if "+2" in pen:
            has_p2 = True

    if has_p2:
        base_ms += 2000

    return base_ms

# ---- Pomocnicze: próba policzenia ruchów/HTM/QTM z adaptera ----
def solve_lengths_from_scramble(state_or_scramble: str) -> Tuple[List[str], int, int, Dict]:
    """
    Próbuje użyć solver_core.kociemba_adapter.solve(state_54).
    Jeśli się nie uda, zwraca pustą listę i 0,0 z info w diagnostics.
    UWAGA: cstimer daje SCRAMBLE (sekwencję mieszania), a adapter zwykle chce stan 54-znakowy.
    Tutaj robimy best-effort: jeśli adapter rzuci wyjątek, zwracamy stub.
    """
    try:
        from solver_core.kociemba_adapter import solve as core_solve
        result = core_solve(state_or_scramble)
        moves = result.get("moves", [])
        htm = int(result.get("length_htm", len(moves)))
        qtm = int(result.get("length_qtm", len(moves)))
        diag = result.get("diagnostics", {})
        diag.update({"source": "adapter"})
        return moves, htm, qtm, diag
    except Exception as e:
        return [], 0, 0, {"source": "import", "note": "no-adapter-or-failed", "error": str(e)}

class Command(BaseCommand):
    help = (
        "Importuje CSV z cstimer do modelu Solve.\n"
        "Zakłada kolumny: time (albo seconds/result/time_ms), scramble (jeśli jest), penalty (opcjonalnie), method (opcjonalnie).\n"
        "Domyślnie ustawia method=LBL jeśli brak kolumny method.\n"
        "Próbuje policzyć HTM/QTM adapterem (opcjonalnie) – jeśli się nie da, zapisze same czasy."
    )

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Ścieżka do CSV z cstimer")
        parser.add_argument("--default-method", default="LBL", help="Metoda, jeśli brak kolumny 'method'")
        parser.add_argument("--col-time", default=None, help="Nazwa kolumny z czasem (gdy nie 'time'/'seconds'/'result'/'time_ms')")
        parser.add_argument("--col-scramble", default=None, help="Nazwa kolumny ze scramble (gdy nie 'scramble')")
        parser.add_argument("--col-penalty", default=None, help="Nazwa kolumny penalty (gdy nie 'penalty')")
        parser.add_argument("--col-method", default=None, help="Nazwa kolumny method (jeśli masz w CSV)")
        parser.add_argument("--dry-run", action="store_true", help="Nie zapisuje do DB, tylko pokazuje ile by dodał")
        parser.add_argument("--use-adapter", action="store_true", help="Spróbuj policzyć HTM/QTM adapterem")

    def handle(self, *args, **opts):
        path = Path(opts["file"])
        if not path.exists():
            raise CommandError(f"CSV not found: {path}")

        col_time = opts["col_time"]
        col_scramble = opts["col_scramble"]
        col_penalty = opts["col_penalty"]
        col_method = opts["col_method"]
        default_method = opts["default_method"]
        dry = opts["dry_run"]
        use_adapter = opts["use_adapter"]

        added, skipped = 0, 0

        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            headers = [h.strip() for h in (reader.fieldnames or [])]

            # Auto-detekcja kolumn, jeśli nie podano
            if not col_time:
                for candidate in ["time", "seconds", "result", "time_ms"]:
                    if candidate in headers:
                        col_time = candidate
                        break
            if not col_scramble:
                for candidate in ["scramble", "scramble_text"]:
                    if candidate in headers:
                        col_scramble = candidate
                        break
            if not col_penalty:
                for candidate in ["penalty", "pen"]:
                    if candidate in headers:
                        col_penalty = candidate
                        break
            if not col_method and "method" in headers:
                col_method = "method"

            if not col_time:
                raise CommandError(f"Nie znalazłem kolumny z czasem w nagłówkach: {headers}")

            self.stdout.write(self.style.NOTICE(
                f"Używam kolumn: time={col_time}, scramble={col_scramble or '-'}, penalty={col_penalty or '-'}, method={col_method or f'(default={default_method})'}"
            ))

            for row in reader:
                raw_time = row.get(col_time)
                raw_pen  = row.get(col_penalty) if col_penalty else None
                ms = parse_time_to_ms(raw_time, raw_pen)

                if ms is None:
                    skipped += 1
                    continue

                method = (row.get(col_method) or default_method) if (col_method or default_method) else "LBL"
                scramble = row.get(col_scramble) if col_scramble else None

                moves, htm, qtm, diag = [], 0, 0, {}
                if use_adapter and scramble:
                    moves, htm, qtm, diag = solve_lengths_from_scramble(scramble)

                if dry:
                    added += 1
                    continue

                Solve.objects.create(
                    method=method,
                    time_ms=ms,
                    moves=json.dumps(moves, ensure_ascii=False),  # TextField przechowuje JSON-string
                    length_htm=htm,
                    length_qtm=qtm,
                )
                added += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import zakończony: dodano {added}, pominięto {skipped} (DNF/brak czasu)."
        ))
        if not use_adapter:
            self.stdout.write(self.style.WARNING(
                "Uwaga: uruchomiłeś bez --use-adapter, więc HTM/QTM = 0. "
                "Możesz je policzyć później, albo powtórzyć import z --use-adapter, jeśli masz adapter."
            ))
