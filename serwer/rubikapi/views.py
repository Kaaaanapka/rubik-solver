import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Solve
from solver_core.kociemba_adapter import solve as core_solve


# --- prosta walidacja stanu 3x3: 54 znaki, tylko URFDLB ---
def validate_state(state: str):
    if not isinstance(state, str):
        return False, "state must be a string"
    state = state.strip()
    if len(state) != 54:
        return False, f"state must be 54 chars, got {len(state)}"
    allowed = set("URFDLB")
    if any(ch not in allowed for ch in state):
        return False, "state contains invalid characters (use only U,R,F,D,L,B)"
    # opcjonalnie: policz wystąpienia (9 na kolor)
    counts = {c: state.count(c) for c in allowed}
    if any(v != 9 for v in counts.values()):
        return False, f"each of U,R,F,D,L,B must occur 9 times, got {counts}"
    return True, "ok"

@api_view(["POST"])
def solve_endpoint(request):
    state = request.data.get("state", "")
    ok, reason = validate_state(state)
    if not ok:
        return Response({
            "moves": [],
            "length_htm": 0,
            "length_qtm": 0,
            "diagnostics": {"valid_state": False, "reason": reason}
        }, status=400)

    # spróbuj użyć adaptera; jeśli brak kociemby, zwróć stub
    try:
        from solver_core.kociemba_adapter import solve as core_solve
        result = core_solve(state)
        # upewnij się, że wynik ma pola:
        moves = result.get("moves", [])
        length_htm = result.get("length_htm", len(moves))
        length_qtm = result.get("length_qtm", len(moves))
        diag = result.get("diagnostics", {})
        diag.update({"valid_state": True, "source": "adapter"})
        return Response({
            "moves": moves,
            "length_htm": length_htm,
            "length_qtm": length_qtm,
            "diagnostics": diag
        })
    except Exception as e:
        # fallback: stub, ale sygnalizujemy, że to tryb mock
        return Response({
            "moves": ["R", "U", "R'", "U'"],
            "length_htm": 4,
            "length_qtm": 4,
            "diagnostics": {"valid_state": True, "source": "stub", "error": str(e)}
        })

@api_view(["POST"])
def submit_solve(request):
    data = request.data
    moves_list = data.get("moves") or []
    time_ms = data.get("time_ms") or 0
    length_htm = data.get("length_htm", len(moves_list))
    length_qtm = data.get("length_qtm", len(moves_list))

    # licz TPS po stronie serwera
    tps = (length_htm / (time_ms/1000.0)) if time_ms else 0.0

    obj = Solve.objects.create(
    method=data.get("method"),
    time_ms=time_ms,
    moves=json.dumps(moves_list, ensure_ascii=False),
    length_htm=length_htm,
    length_qtm=length_qtm,
    state_54=data.get("state")  # tu dodajemy
)

    return Response({"status": "ok", "id": obj.id, "tps": round(tps, 3)})