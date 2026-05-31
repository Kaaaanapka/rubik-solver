import cv2
import numpy as np 

#UKŁAD ŚCIAN KOSTKI GÓRNA LEWA PRAWA FRONT TYLNIA ETC
#      U
#    L F R B
#      D
#UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'

#Najpierw:
#U - gorna
#R - prawa 
#F - front
#D - dolna
#L - lewa
#B - tylna

def naklejka():

    size = 50       #Rozmiar naklejki
    margin = 5      #Odstęp
    odstep = margin * 3  # Większy odstęp między ściankami

    # Tworzymy tło
    img_size = (size * 15, size * 11)
    img = np.ones((img_size[1], img_size[0],3), dtype=np.uint8) * 50      #Uzywamy palety BGR bo CV2 bazuje na BGR (Szare tło do łatwego odczytania naklejek)

    kolory = {

        "Bialy" : (255,255,255),
        "Zolty" : (0, 255, 255),
        "Czerwony" : (0, 0, 255),
        "Pomaranczowy" : (0, 165, 255),
        "Zielony" : (0, 255, 0),
        "Niebieski" : (255, 0, 0),
        "Czarny": (0,0,0)       #Dodanie czarnego koloru dla obramowki

    }

    pozycja_scianki = {
        "U": (size * 4 + odstep, size),      # Góra
        "L": (size, size * 4 + odstep),      # Lewo
        "F": (size * 4 + odstep, size * 4 + odstep),  # Przód
        "R": (size * 7 + 2 * odstep, size * 4 + odstep),  # Prawo
        "B": (size * 10 + 3 * odstep, size * 4 + odstep), # Tył
        "D": (size * 4 + odstep, size * 7 + 2 * odstep),  # Dół
    }

    kolory_scianek = {
        "U": "Bialy",
        "D": "Zolty",
        "L": "Czerwony",
        "R": "Pomaranczowy",
        "F": "Zielony",
        "B": "Niebieski"
    }

    # Rysowanie naklejek facelet'ów

    for scianka, (start_x, start_y) in pozycja_scianki.items():
        kolor = kolory[kolory_scianek[scianka]]


        for row in range(3):            #Generowanie 3 wierszy
            for col in range(3):        #Generowanie 3 kolumn
                x = start_x + col * (size + margin)
                y = start_y + row * (size + margin)
                # #kolor = kolory['Bialy']
                # kolor = kolory[['Bialy', 'Czerwony', 'Niebieski'][row]]
                cv2.rectangle(img, (x, y), (x + size, y + size), kolor, -1)   #Nakljeka (wypełniony kwadrat)
                cv2.rectangle(img, (x, y), (x + size, y + size), kolory["Czarny"], 2)    #Obwód kwadratu czarny

    cv2.imshow("Facelet 2D", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows


#Do testu facelet.py
#naklejka()