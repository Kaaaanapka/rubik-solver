# serwer/solver_core/kociemba_adapter.py
import traceback
import twophase.solver as sv
from typing import List


print("[adapter] loaded twophase adapter")

def normalize_moves(moves: List[str]) -> List[str]:
    normalized = []
    for m in moves:
        if m.endswith("3"):
            normalized.append(m[0] + "'")   # np. U3 -> U'
        elif m.endswith("1"):
            normalized.append(m[0])        # np. D1 -> D
        elif m.endswith("0"):
            continue                       # np. U0 -> pomijamy
        else:
            normalized.append(m)           # zostaw resztę bez zmian
    return normalized
def solve(state_54: str) -> dict:
    print("[adapter] solve called, len=", len(state_54))
    try:
        sol = sv.solve(state_54, 21, 5)  # bezpieczne parametry
        moves = sol.split()
        moves = normalize_moves(moves)   # zamiana U3 -> U'
        print("Rozwiązanie kostki:", " ".join(moves)) 
        return {
            "moves": moves,
            "length_htm": len(moves),
            "length_qtm": sum(2 if m.endswith("2") else 1 for m in moves),
            "diagnostics": {"source": "twophase", "ok": True}
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "moves": ["R", "U", "R'", "U'"],
            "length_htm": 4,
            "length_qtm": 4,
            "diagnostics": {"source": "stub", "error": str(e)}
        }
    