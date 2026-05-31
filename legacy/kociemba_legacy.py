import twophase.solver as sv  # Importujemy solver twophase.solver


#UKŁAD ŚCIAN KOSTKI GÓRNA LEWA PRAWA FRONT TYLNIA ETC
#      U
#    L F R B
#      D

def Kociemba(canvas, wszystkie_naklejki):
    from GUI import pokaz_kolor             #Importowanie z GUI funkcji pokaz_kolory po to aby nie doszło do loop'a importów co miało miejsce wcześniej
    #Pobieramy kod_kostki z pokaz_kolor
    kod_kostki = pokaz_kolor(canvas, wszystkie_naklejki)

    # Debugowanie sprawdzamy czy kod_kostki zwraca poprawne wartości
    # print("Kod kostki:", kod_kostki)

    try: 
        rozwiazanie = sv.solve(kod_kostki, 19, 2)
        print("Rozwiazanie kostki:", rozwiazanie) 
        return rozwiazanie
    except Exception as e:
        print("Błąd przy rozwiązywaniu kostki:", e)
        return None

