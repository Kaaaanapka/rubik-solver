import sys, csv
import matplotlib.pyplot as plt
from collections import defaultdict

if len(sys.argv) < 2:
    print("Usage: python scripts/analyze_csv.py data/solves.csv")
    sys.exit(1)

rows = []
with open(sys.argv[1], newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        row["time_ms"] = int(row.get("time_ms") or 0)
        row["length_htm"] = int(row.get("length_htm") or 0)
        row["length_qtm"] = int(row.get("length_qtm") or 0)
        row["tps"] = float(row.get("tps") or 0.0)
        row["method"] = row.get("method") or ""
        rows.append(row)

# Grupowanie po metodzie
by_method = defaultdict(list)
for row in rows:
    by_method[row["method"]].append(row["time_ms"])

# Boxplot czasów
plt.figure()
plt.boxplot([by_method[m] for m in by_method], labels=list(by_method.keys()), showmeans=True)
plt.title("Time (ms) by Method")
plt.ylabel("Time (ms)")
plt.savefig("box_time_by_method.png", dpi=144)

# Scatter: HTM vs czas
plt.figure()
plt.scatter([r["length_htm"] for r in rows], [r["time_ms"] for r in rows], alpha=0.6)
plt.title("HTM vs Time")
plt.xlabel("HTM")
plt.ylabel("Time (ms)")
plt.savefig("scatter_htm_vs_time.png", dpi=144)

print("Saved plots: box_time_by_method.png, scatter_htm_vs_time.png")
