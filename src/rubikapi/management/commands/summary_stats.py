from django.core.management.base import BaseCommand, CommandError
from rubikapi.models import Solve
import statistics

def p95(data):
    if not data:
        return None
    data_sorted = sorted(data)
    k = int(round(0.95 * (len(data_sorted)-1)))
    return data_sorted[k]

class Command(BaseCommand):
    help = "Print per-method summary stats (count, median, p95, mean HTM/QTM, avg TPS)."

    def handle(self, *args, **options):
        methods = Solve.objects.values_list("method", flat=True).distinct()
        if not methods:
            self.stdout.write("No solves.")
            return

        header = f"{'Method':<10} {'n':>5} {'Median(ms)':>12} {'p95(ms)':>10} {'meanHTM':>8} {'meanQTM':>8} {'avgTPS':>8}"
        self.stdout.write(header)
        self.stdout.write("-"*len(header))

        for m in methods:
            qs = Solve.objects.filter(method=m)
            times = [s.time_ms for s in qs if s.time_ms is not None]
            htms = [s.length_htm for s in qs]
            qtms = [s.length_qtm for s in qs]
            tps = [ (s.length_htm/(s.time_ms/1000.0)) for s in qs if s.time_ms and s.time_ms>0 ]
            med = statistics.median(times) if times else None
            p95v = p95(times) if times else None
            mean_htm = statistics.mean(htms) if htms else None
            mean_qtm = statistics.mean(qtms) if qtms else None
            avg_tps = statistics.mean(tps) if tps else None
            self.stdout.write(f"{(m or ''):<10} {qs.count():>5} {str(med or ''):>12} {str(p95v or ''):>10} {str(round(mean_htm,2) if mean_htm is not None else ''):>8} {str(round(mean_qtm,2) if mean_qtm is not None else ''):>8} {str(round(avg_tps,2) if avg_tps is not None else ''):>8}")
