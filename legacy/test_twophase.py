import twophase.solver as sv

state = "UUUUUUUUUFFFRRRRRRLLLFFFFFFDDDDDDDDDBBBLLLLLLRRRBBBBBB"

print("Wejście:", state)
try:
    sol = sv.solve(state, 21, 5)
    print("Rozwiązanie:", sol)
except Exception as e:
    print("Błąd:", e)