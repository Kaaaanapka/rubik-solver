import tkinter as tk
from kamera import uruchom_kamere
#from facelet import naklejka
#from kociemba import Kociemba
from kolory import kolor_scianek, mapowanie_kolorow
import random
from scramble import generuj_scramble
import argparse
import json, requests, time

API = "http://127.0.0.1:8000/api"

# stan aplikacji (zapamiętujemy ostatni stan/ruchy/pomiar)
LAST_STATE = ""
LAST_SOLUTION = {}   # {"moves": [...], "length_htm": int, "length_qtm": int}
START_TS = None      # time.time() kiedy start pomiaru
DEFAULT_METHOD = "LBL"  # możesz podmienić w GUI dropdownem



# --- Bufor ruchów i liczniki HTM/QTM ---
MOVES = []                 # lista stringów, np. ["R","U","R'","U'"]
CROSS_HTM_MANUAL = 0       # jeśli chcesz ręcznie dopisać HTM za krzyż

FACE_ORDER = ["U","R","F","D","L","B"]
FACE_IDXS  = [0,   3,   2,   5,   1,   4]  # indeksy w liście [naklejki1..naklejki6] odpowiadające powyższym literom

def zbuduj_state_54(canvas, wszystkie_naklejki):
    parts = []
    # ułóż twój „wszystkie_naklejki” w kolejności U,R,F,D,L,B
    faces_ordered = [wszystkie_naklejki[i] for i in FACE_IDXS]
    for face_squares in faces_ordered:
        for sq_id in face_squares:
            tk_color = canvas.itemcget(sq_id, "fill")
            lit = mapowanie_kolorow.get(tk_color)
            if not lit:
                lit = "?"  # nieznany kolor -> błąd
            parts.append(lit)
    return "".join(parts)

def fmt_time_str(ms: int) -> str:
    total_ms = int(ms)
    m = total_ms // 60000
    s = (total_ms % 60000) // 1000
    x = total_ms % 1000
    return f"{m:02d}:{s:02d}.{x:03d}"

def add_macro(seq):
    """Dodaj makro (lista ruchów)."""
    MOVES.extend(seq)

def clear_moves():
    """Wyczyść sekwencję."""
    MOVES.clear()

def htm_qtm(moves):
    """Policz HTM/QTM z listy ruchów (ignoruje rotacje x/y/z)."""
    htm = sum(1 for m in moves if m and m[0] not in ("x","y","z"))
    qtm = sum(2 if isinstance(m, str) and m.endswith("2") else 1 for m in moves if m and m[0] not in ("x","y","z"))
    return htm, qtm

# --- Makra LBL wg Twojego planu ---
MACROS = {
    "F2L_basic":   ["R", "U", "R'", "U'"],
    "S2_right":    ["U", "R", "U'", "R'", "U'", "F'", "U", "F"],
    "S2_left":     ["U'", "L'", "U", "L", "U", "F", "U'", "F'"],
    "OLL_cross":   ["F", "R", "U", "R'", "U'", "F'"],
    "OLL_corners": ["R", "U", "R'", "U'"],
    "PLL_corners": ["R'", "U", "R'", "D2", "R", "U'", "R'", "D2", "R2"],
    "PLL_edges":   ["M2", "U", "M", "U2", "M'", "U", "M2"],
}

def apply_macro(name):
    add_macro(MACROS[name])

def api_solve(state_54: str) -> dict:
    resp = requests.post(f"{API}/solve", json={"state": state_54}, timeout=10)
    resp.raise_for_status()
    return resp.json()

def api_submit_solve(method: str, time_ms: int, state_54: str, solution: dict) -> dict:
    moves = solution.get("moves", [])
    htm = solution.get("length_htm", len(moves))
    qtm = solution.get("length_qtm", len(moves))
    payload = {
        "method": method,
        "time_ms": time_ms,
        "moves": moves,
        "length_htm": htm,
        "length_qtm": qtm,
        "state": state_54,
    }
    resp = requests.post(f"{API}/submit_solve", json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()

#zmienna globalna przechowujaca aktualny kolor
aktualny_kolor = "white"

# Funkcja do generowania faceletów na każdej ściance
def generuj_naklejke(canvas, start_x, start_y, kolor="white"):
    rozmiar = 50
    margin = 5
    naklejki = []

    for i in range(3):
        for j in range(3):
            x = start_x + j * (rozmiar + margin)
            y = start_y + i * (rozmiar + margin)
            kwadrat = canvas.create_rectangle(x, y, x + rozmiar, y + rozmiar, fill=kolor, outline="black")

            canvas.itemconfig(kwadrat, fill=kolor)  # Wymuszenie ustawienia koloru
            naklejki.append(kwadrat)        #Dodaje ID naklejki do listy

            # Poprawione - używa poprawnej funkcji
            canvas.tag_bind(kwadrat, "<Button-1>", lambda event, canvas=canvas, kw=kwadrat: wypelnij(event, canvas, kw))

    return naklejki

#Funkcja do wypelnienia kwadracika kolorkiem (naklejki)
def wypelnij(event, canvas, kwadrat):

    global aktualny_kolor
    item = canvas.find_closest(event.x, event.y)[0]  # Znajduje najbliższy obiekt
    canvas.itemconfig(item, fill=aktualny_kolor)  # Zmienia jego kolor

#Funkcja do zmiany kolorow pojedynczej naklejki
def zmien_kolor(nowy_kolor):

    global aktualny_kolor
    aktualny_kolor = nowy_kolor

#Funkcja do odczytywanie kolorow z naklejek dla kociemba.py w celu rozwiazania kostki
def odczytaj_kolor(canvas, naklejki):
    kolory = []
    for naklejka in naklejki:
        kolor = canvas.itemcget(naklejka, "fill")       #Pobiera aktualny kolor naklejki

        #print(f"ID Naklejki: {naklejka}, Kolor: {kolor}")  # Debugowanie

        kolory.append(mapowanie_kolorow.get(kolor, "?"))  # Mapowanie na oznaczenie Kociemby
        

    return "".join(kolory)      #Łaczy w ciąg znaków

def reset_kostka(canvas, wszystkie_naklejki, label_rozwiaz, label_scramble=None):
    """
    Przywraca domyślne kolory naklejek i czyści stan aplikacji.
    Kolejność ścian odpowiada tej, w której je rysujesz w main():
      1: white (U), 2: red (R), 3: green (F), 4: yellow (D), 5: orange (L), 6: blue (B)
    """
    global MOVES, CROSS_HTM_MANUAL, LAST_STATE, LAST_SOLUTION, START_TS

    default_face_colors = ["white", "red", "green", "yellow", "orange", "blue"]

    # Ustaw kolor dla każdej ścianki z osobna
    for face_idx, face_squares in enumerate(wszystkie_naklejki):
        kolor = default_face_colors[face_idx]
        for sq_id in face_squares:
            canvas.itemconfig(sq_id, fill=kolor)

    # Wyczyść stan aplikacji
    MOVES.clear()
    CROSS_HTM_MANUAL = 0
    LAST_STATE = ""
    LAST_SOLUTION = {}
    START_TS = None

    # Odśwież etykiety
    if label_rozwiaz is not None:
        label_rozwiaz.config(text="Rozwiązanie kostki to: ")
    if label_scramble is not None:
        label_scramble.config(text="Twój scramble to: ")

#Pokazuje cubestring (kod_kostki) po wprowadzeniu kolorow
def pokaz_kolor(canvas, wszystkie_naklejki, label_rozwiaz):
    global LAST_STATE, LAST_SOLUTION
    wszystkie_naklejki_flat = [id for sciana in wszystkie_naklejki for id in sciana]
    kod_kostki = odczytaj_kolor(canvas, wszystkie_naklejki_flat)
    print("Kolory scianki:", kod_kostki)
    LAST_STATE = kod_kostki

    # policz ruchy przez backend i pokaż w labelu
    try:
        result = api_solve(LAST_STATE)
        LAST_SOLUTION = {
            "moves": result.get("moves", []),
            "length_htm": result.get("length_htm", 0),
            "length_qtm": result.get("length_qtm", 0),
        }
        pretty = " ".join(LAST_SOLUTION["moves"]) or "(brak)"
        label_rozwiaz.config(text=f"Rozwiązanie kostki to: {pretty}")
    except Exception as e:
        label_rozwiaz.config(text=f"Błąd /api/solve: {e}")
        LAST_SOLUTION = {}

    return kod_kostki
    
def rozwiaz_kostke(label, canvas, wszystkie_naklejki):
    rozwiazanie = Kociemba(canvas, wszystkie_naklejki)
    label.config(text=f"Rozwiazanie kostki to {rozwiazanie}")

def pokaz_scramble(label):
    scramble = generuj_scramble()  
    label.config(text=f'Twój scramble to: {scramble}')

def start_pomiaru(label_rozwiaz):
    global START_TS
    START_TS = time.time()
    label_rozwiaz.config(text="Pomiar rozpoczęty… Układaj!")

def zapisz_wynik(label_rozwiaz):
    global START_TS, LAST_STATE, LAST_SOLUTION, MOVES
    if START_TS is None:
        label_rozwiaz.config(text="Najpierw kliknij: Start pomiaru")
        return
    if not LAST_STATE:
        label_rozwiaz.config(text="Najpierw kliknij: Oblicz ruchy / Pokaż kod kostki")
        return

    elapsed_ms = int((time.time() - START_TS) * 1000)

    # policz lokalnie z bufora MOVES (nie z LAST_SOLUTION)
    h_local, q_local = htm_qtm(MOVES)

    payload = {
        "method": DEFAULT_METHOD,
        "time_ms": elapsed_ms,
        "moves": MOVES,          # pełna sekwencja z makr
        "length_htm": h_local,   # możesz wysłać 0 – backend i tak policzy
        "length_qtm": q_local,
        "state": LAST_STATE
    }

    try:
        resp = requests.post(f"{API}/submit_solve", json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()  # <--- KLUCZOWE
        rec_id = data.get("id", "?")   # backend może nie zwracać id
        label_rozwiaz.config(
            text=f"Zapisano: {fmt_time_str(elapsed_ms)} (id={rec_id}, HTM={h_local})"
        )
        # reset po zapisie
        clear_moves()
        START_TS = None
    except Exception as e:
        label_rozwiaz.config(text=f"Błąd zapisu: {e}")


# Funkcja do dodawania przycisków
def dodaj_przycisk(root, canvas, wszystkie_naklejki):
    label_rozwiaz = tk.Label(root, text="Rozwiązanie kostki to: ", font=("Arial", 15))
    label_rozwiaz.pack(pady=5)

    label_scramble = tk.Label(root, text="Twój scramble to: ", font=("Arial", 13))
    label_scramble.pack(pady=5)

    kamera = tk.Button(root, text="Uruchom kamerę", command=lambda: uruchom_kamere())
    kamera.pack(pady=5)

    scramble_btn = tk.Button(root, text="Generuj scramble", command=lambda: pokaz_scramble(label_scramble))
    scramble_btn.pack(pady=5)

    # zamiast starego "Pokaz kod kostki" bez API – robimy "Oblicz ruchy"
    oblicz_btn = tk.Button(
        root, text="Oblicz ruchy",
        command=lambda: pokaz_kolor(canvas, wszystkie_naklejki, label_rozwiaz)
    )
    oblicz_btn.pack(pady=5)

    start_btn = tk.Button(root, text="Start pomiaru", command=lambda: start_pomiaru(label_rozwiaz))
    start_btn.pack(pady=5)

    zapisz_btn = tk.Button(root, text="Zapisz wynik", command=lambda: zapisz_wynik(label_rozwiaz))
    zapisz_btn.pack(pady=5)

    # (opcjonalnie) zostaw swój legacy przycisk do lokalnego solvera:
    # rozwiaz = tk.Button(root, text="Rozwiaz kostke", command=lambda: rozwiaz_kostke(label_rozwiaz, canvas, wszystkie_naklejki))
    # rozwiaz.pack(pady=5)
    reset_btn = tk.Button(
        root, text="Reset kostki",
        command=lambda: reset_kostka(canvas, wszystkie_naklejki, label_rozwiaz, label_scramble)
    )
    reset_btn.pack(pady=5)
    
        # --- Guziki do makr ---
    frm = tk.Frame(root)
    frm.pack(pady=6)

    tk.Button(frm, text="F2L narożnik",     command=lambda: apply_macro("F2L_basic")).pack(side=tk.LEFT, padx=3)
    tk.Button(frm, text="S2 prawa",         command=lambda: apply_macro("S2_right")).pack(side=tk.LEFT, padx=3)
    tk.Button(frm, text="S2 lewa",          command=lambda: apply_macro("S2_left")).pack(side=tk.LEFT, padx=3)
    tk.Button(frm, text="OLL krzyż",        command=lambda: apply_macro("OLL_cross")).pack(side=tk.LEFT, padx=3)
    tk.Button(frm, text="OLL rogi",         command=lambda: apply_macro("OLL_corners")).pack(side=tk.LEFT, padx=3)
    tk.Button(frm, text="PLL rogi",         command=lambda: apply_macro("PLL_corners")).pack(side=tk.LEFT, padx=3)
    tk.Button(frm, text="PLL krawędzie",    command=lambda: apply_macro("PLL_edges")).pack(side=tk.LEFT, padx=3)

    # Podgląd HTM/QTM i liczby ruchów
    info = tk.Label(root, text="HTM=0, QTM=0 | Ruchów: 0")
    info.pack(pady=4)

    def refresh_info():
        h, q = htm_qtm(MOVES)
        info.config(text=f"HTM={h}  QTM={q}  |  Ruchów: {len(MOVES)}")
        root.after(300, refresh_info)
    refresh_info()

    # Opcjonalnie: cofanie i czyszczenie bufora
    ctl = tk.Frame(root); ctl.pack(pady=4)
    tk.Button(ctl, text="Wyczyść sekwencję", command=clear_moves).pack(side=tk.LEFT, padx=3)



# Funkcja do dodawania kwadracików z kolorami
def dodaj_kwadracik(root):

    global aktualny_kolor
    
    frame = tk.Frame(root)
    frame.pack(pady=5)

    for kolor in kolor_scianek:
        przycisk = tk.Button(frame, width=5, height=2, bg=kolor, bd=1, command=lambda k=kolor: zmien_kolor(k))
        przycisk.pack(side=tk.LEFT, padx=2)

# Główna funkcja aplikacji
def main():
    
    global aktualny_kolor

    root = tk.Tk()

    root.title ('Aplikacja do kostki rubika')       # Tytuł okna
    
    root.geometry('1800x1200',)           # Wymiary okna
    canvas = tk.Canvas(root, width=750, height=530)  # Canvas do rysowania
    canvas.pack()



    # Rysowanie pustych ścianek kostki (teraz są one niezależne)
    naklejki1 = generuj_naklejke(canvas, 220, 20, 'white')  # 1. Ścianka
    naklejki2 = generuj_naklejke(canvas, 390, 190, 'red')  # 2. Ścianka
    naklejki3 = generuj_naklejke(canvas, 220, 190, 'green')  # 3. Ścianka
    naklejki4 = generuj_naklejke(canvas, 220, 360, 'yellow')  # 4. Ścianka
    naklejki5 = generuj_naklejke(canvas, 50, 190, 'orange')  # 5. Ścianka
    naklejki6 = generuj_naklejke(canvas, 560, 190, 'blue')  # 6. Ścianka

    wszystkie_naklejki = [naklejki1, naklejki2, naklejki3, naklejki4, naklejki5, naklejki6]

    # Uruchomienie pętli głównej aplikacji
    dodaj_przycisk(root, canvas, wszystkie_naklejki)
    dodaj_kwadracik(root)

    root.mainloop()

    #Dodane nowe!!!!
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-new-core", action="store_true", help="Use solver_core instead of legacy")
    args = parser.parse_args()

    # Tutaj pobierasz state_54 (np. z kamery, albo na razie na sztywno)
    state_54 = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

    if args.use_new_core:
        from solver_core.kociemba_adapter import solve
        result = solve(state_54)
        print("Moves:", " ".join(result.get("moves", [])))
        print("HTM:", result.get("length_htm"), "QTM:", result.get("length_qtm"))
    
# Uruchom aplikację
if __name__ == "__main__":
    main()
