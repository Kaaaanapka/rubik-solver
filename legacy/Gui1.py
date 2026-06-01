import tkinter as tk
from kamera import uruchom_kamere
from _legacy.facelet import naklejka


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

            naklejki.append({"x": x, "y": y, "kwadrat": kwadrat, "kolor": kolor})

            # Poprawione - używa poprawnej funkcji
            canvas.tag_bind(kwadrat, "<Button-1>", lambda event, canvas=canvas: wypelnij(event, canvas))

    return naklejki


def wypelnij(event, canvas):
    global aktualny_kolor
    item = canvas.find_closest(event.x, event.y)[0]  # Znajduje najbliższy obiekt
    canvas.itemconfig(item, fill=aktualny_kolor)  # Zmienia jego kolor


def zmien_kolor(kolor):
    global aktualny_kolor
    aktualny_kolor = kolor

# Funkcja do dodawania przycisków
def dodaj_przycisk(root, canvas):       
    kamera = tk.Button(root, text="Uruchom kamerę", command=lambda: uruchom_kamere()) 
    kamera.pack(pady=5)

    facelet = tk.Button(root, text="Wyswietl naklejke", command=lambda: naklejka())
    facelet.pack(pady=5)

    gen_naklejka = tk.Button(root, text='Pokoloruj naklejke', command=lambda: generuj_naklejke(canvas, 220, 50, aktualny_kolor))
    gen_naklejka.pack(pady=5)

# Funkcja do dodawania kwadracików z kolorami
def dodaj_kwadracik(root, canvas):
    # Czerwony kwadrat (Button z tłem czerwonym)
    czerwony = tk.Button(root, width=5, height=2, bg="red", bd=1, command=lambda: zmien_kolor("red"))
    czerwony.pack(pady=5)

    # Niebieski kwadrat
    niebieski = tk.Button(root, width=5, height=2, bg="blue", bd=1, command=lambda: zmien_kolor("blue"))
    niebieski.pack(pady=5)

    # Żółty kwadrat
    zolty = tk.Button(root, width=5, height=2, bg="yellow", bd=1, command=lambda: zmien_kolor("yellow"))
    zolty.pack(pady=5)

    # Zielony kwadrat
    zielony = tk.Button(root, width=5, height=2, bg="green", bd=1, command=lambda: zmien_kolor("green"))
    zielony.pack(pady=5)

    # Pomarańczowy kwadrat
    pomaranczowy = tk.Button(root, width=5, height=2, bg="orange", bd=1, command=lambda: zmien_kolor("orange"))
    pomaranczowy.pack(pady=5)

    # Biały kwadrat
    bialy = tk.Button(root, width=5, height=2, bg="white", bd=1, command=lambda: zmien_kolor("white"))
    bialy.pack(pady=5)


# Główna funkcja aplikacji
def main():
    
    global aktualny_kolor
    aktualny_kolor = "white"  # Domyślny kolor pędzla

    root = tk.Tk()

    root.title ('Aplikacja do kostki rubika')       # Tytuł okna
    
    root.geometry('1800x1200',)           # Wymiary okna
    canvas = tk.Canvas(root, width=750, height=600, bg='white')  # Canvas do rysowania
    canvas.pack()

    # Rysowanie pustych ścianek kostki (teraz są one niezależne)
    naklejki1 = generuj_naklejke(canvas, 220, 50, aktualny_kolor)  # 1. Ścianka
    naklejki2 = generuj_naklejke(canvas, 220, 220, aktualny_kolor)  # 2. Ścianka
    naklejki3 = generuj_naklejke(canvas, 50, 220, aktualny_kolor)  # 3. Ścianka
    naklejki4 = generuj_naklejke(canvas, 390, 220, aktualny_kolor)  # 4. Ścianka
    naklejki5 = generuj_naklejke(canvas, 560, 220, aktualny_kolor)  # 5. Ścianka
    naklejki6 = generuj_naklejke(canvas, 220, 390, aktualny_kolor)  # 6. Ścianka

    # Uruchomienie pętli głównej aplikacji
    dodaj_przycisk(root, canvas)
    dodaj_kwadracik(root, canvas)

    root.mainloop()

# Uruchom aplikację
if __name__ == "__main__":
    main()
