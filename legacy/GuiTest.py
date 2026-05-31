import tkinter as tk
from kamera import uruchom_kamere
from facelet import naklejka
from kociemba import Kociemba
from kolory import kolor_scianek, mapowanie_kolorow
import random
from scramble import generuj_scramble

#zmienna globalna przechowujaca aktualny kolor
aktualny_kolor = "white"

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

def zaktualizuj_scianke(canvas, wszystkie_naklejki, kolory_z_kamery):
    """
    kolory_z_kamery: lista 9 kolorów wykrytych przez kamerę (np. ['blue', 'blue', ..., 'blue'])
    """
    if len(kolory_z_kamery) != 9:
        print("Niepoprawna liczba kolorów z kamery!")
        return

    # Środek ścianki to element nr 4
    kolor_srodka = kolory_z_kamery[4]
    indeks_scianki = kolor_scianek.index(kolor_srodka) if kolor_srodka in kolor_scianek else None

    if indeks_scianki is None:
        print("Nierozpoznany kolor środka:", kolor_srodka)
        return

    naklejki = wszystkie_naklejki[indeks_scianki]

    for i in range(9):
        canvas.itemconfig(naklejki[i], fill=kolory_z_kamery[i])


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

#Pokazuje cubestring (kod_kostki) po wprowadzeniu kolorow
def pokaz_kolor(canvas, wszystkie_naklejki):
    wszystkie_naklejki_flat = [id for sciana in wszystkie_naklejki for id in sciana]  # Spłaszczenie listy
    kod_kostki = odczytaj_kolor(canvas, wszystkie_naklejki_flat)
    print("Kolory scianki:", kod_kostki)
    return kod_kostki
    
def rozwiaz_kostke(label, canvas, wszystkie_naklejki):
    rozwiazanie = Kociemba(canvas, wszystkie_naklejki)
    label.config(text=f"Rozwiazanie kostki to {rozwiazanie}")

def pokaz_scramble(label):
    scramble = generuj_scramble()  
    label.config(text=f'Twój scramble to: {scramble}')

# Funkcja do dodawania przycisków
def dodaj_przycisk(root, canvas, wszystkie_naklejki):       
    kamera = tk.Button(root, text="Uruchom kamerę", command=lambda: uruchom_kamere()) 
    kamera.pack(pady=5)

    facelet = tk.Button(root, text="Wyswietl naklejke", command=lambda: naklejka())
    facelet.pack(pady=5)

    scramble = tk.Button(root, text="Generuj scramble", command=lambda: pokaz_scramble(label_scramble))
    scramble.pack(pady=5)

    pokaz_kolory = tk.Button(root, text="Pokaz kod kostki", command=lambda: pokaz_kolor(canvas, wszystkie_naklejki))
    pokaz_kolory.pack(pady=5)

    label_rozwiaz = tk.Label(root, text="Rozwiązanie kostki to: ", font=("Arial", 15))
    label_rozwiaz.pack(pady=5)
    #label_rozwiaz.place(x = 10, y = 50)

    label_scramble = tk.Label(root, text="Twój scramble to: ", font=("Arial", 13))
    label_scramble.pack(pady=5)
    

    rozwiaz = tk.Button(root, text="Rozwiaz kostke", command=lambda: rozwiaz_kostke(label_rozwiaz, canvas, wszystkie_naklejki))
    rozwiaz.pack(pady=5)



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
    canvas = tk.Canvas(root, width=750, height=600)  # Canvas do rysowania
    canvas.pack()



    # Rysowanie pustych ścianek kostki (teraz są one niezależne)
    naklejki1 = generuj_naklejke(canvas, 220, 50, 'white')  # 1. Ścianka
    naklejki2 = generuj_naklejke(canvas, 390, 220, 'red')  # 2. Ścianka
    naklejki3 = generuj_naklejke(canvas, 220, 220, 'green')  # 3. Ścianka
    naklejki4 = generuj_naklejke(canvas, 220, 390, 'yellow')  # 4. Ścianka
    naklejki5 = generuj_naklejke(canvas, 50, 220, 'orange')  # 5. Ścianka
    naklejki6 = generuj_naklejke(canvas, 560, 220, 'blue')  # 6. Ścianka

    wszystkie_naklejki = [naklejki1, naklejki2, naklejki3, naklejki4, naklejki5, naklejki6]

    # Uruchomienie pętli głównej aplikacji
    dodaj_przycisk(root, canvas, wszystkie_naklejki)
    dodaj_kwadracik(root)

    root.mainloop()

# Uruchom aplikację
if __name__ == "__main__":
    main()
