

import cv2
import numpy as np

kolory = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]  # Kolory dla warstw

def wykryj(frame, pozycja):
    
    for i, (x, y) in enumerate(pozycja):
        cv2.rectangle(frame, (x, y), (x + 15, y + 15), kolory[i // 3], 2)

    x_start = x
    x_end = x + 15
    y_start = y
    y_end = y + 15
    roi_1 = frame[y_start:y_end, x_start:x_end]

    # # ========================================================= HSV

        # Przykładowe operacje na każdym małym kwadraciku
        # Konwersja do HSV
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(roi_1, cv2.COLOR_BGR2HSV)

        # Możesz teraz używać tego małego regionu (roi_small) do dalszych operacji
        # np. maskowanie, detekcja kolorów itp.

# ========================================================= KOLORY



    # Definicja kolorów kostki (dla koloru czerwonego)
    dolny_red_1 = np.array([0, 100, 100])  # Parametry HSV dolne dla koloru czerwonego
    gorny_red_1 = np.array([5, 255, 255])  # Parametry HSV górne

    dolny_red_2 = np.array([170, 100, 100])  # Parametry HSV dolne
    gorny_red_2 = np.array([179, 255, 255])  # Parametry HSV górne

    #Definicja kolorów kostki (dla koloru zielonego)

    dolny_ziel = np.array([45, 100, 100])      # Parametry HSV dolne zielony
    gorny_ziel = np.array([85, 255, 255])    # Parametry HSV górne zielony


    #Definicja kolorow dla zoltego

    dolny_zolty = np.array([25, 100, 100])  # Dolne wartości dla koloru żółtego w HSV
    gorny_zolty = np.array([32, 255, 255])  # Górne wartości dla koloru żółtego w HSV

    #Definicja HSV dla koloru pomarańczowego
    dolny_orange = np.array([5, 100, 100])  # Zmniejszamy nasycenie
    gorny_orange = np.array([20, 255, 255])  # Zmniejszamy zakres

    #HSV dla białego

    dolny_bialy = np.array([0, 0, 200])  # Ustawienie na szerszy zakres
    gorny_bialy = np.array([180, 30, 255])

    #HSV dla niebieskiego

    dolny_nieb = np.array([90, 50, 50])   # Wartości mogą wymagać korekty
    gorny_nieb = np.array([130, 255, 255])

    # Tworzenie masek 
    maska_red_1 = cv2.inRange(hsv, dolny_red_1, gorny_red_1)
    maska_red_2 = cv2.inRange(hsv, dolny_red_2, gorny_red_2)

    maska_ziel = cv2.inRange(hsv, dolny_ziel, gorny_ziel)

    maska_zolty = cv2.inRange(hsv, dolny_zolty, gorny_zolty)

    maska_orange = cv2.inRange(hsv, dolny_orange, gorny_orange)

    maska_biala = cv2.inRange(hsv, dolny_bialy, gorny_bialy)

    maska_nieb = cv2.inRange(hsv, dolny_nieb, gorny_nieb)

#==========================================================================================

    # Łączenie masek czerwonych
    maska_red_all = cv2.bitwise_or(maska_red_1, maska_red_2)                    #polaczona maska_red_1 i maska_red_2 
    maska_Red_Ziel = cv2.bitwise_or(maska_red_all, maska_ziel)                   #cv2.bitwise_or przyjmuje tylko dwa argumenty dlatego je trzeba cześciami łaczyć
    maska_Zol_Ora = cv2.bitwise_or(maska_zolty, maska_orange)
    maska_RZZO = cv2.bitwise_or(maska_Red_Ziel, maska_Zol_Ora)                  #polaczenie masek Red_Ziel z Zol_Ora (bo tylko dwa parametry przyjmuje cv2.bitwise_or)\
    maska_Bia_Nie = cv2.bitwise_or(maska_biala, maska_nieb)
    maska_all = cv2.bitwise_or(maska_RZZO, maska_Bia_Nie)


    # Sprawdzamy, czy w obrębie ROI znajduje się kolor dany kolor

    if np.any(maska_red_all):  # Jeśli istnieją jakiekolwiek białe piksele w masce (czyli kolor czerwony jest obecny)
        cv2.putText(frame, "Czer", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
       
    if np.any(maska_ziel): 
        cv2.putText(frame, "Ziel", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
   
    if np.any(maska_zolty): 
        cv2.putText(frame, "Zolty", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
    if np.any(maska_orange):
        cv2.putText(frame, "Pom", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) 

    if np.any(maska_biala):
        cv2.putText(frame, "Bialy", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) 

    if np.any(maska_nieb):
        cv2.putText(frame, "Nieb", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) 

        # Znajdowanie konturów w masce
        contours, _ = cv2.findContours(maska_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        # Rysowanie konturów na obrazie ROI
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filtrujemy małe kontury
                x, y, w, h = cv2.boundingRect(contour)
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Rysowanie prostokąta na obrazie 'frame'
                cv2.rectangle(frame, (x + x_start, y + y_start), (x + x_start + w, y + y_start + h), (0, 255, 0), 2)

    cv2.imshow("Maska czerwonego", maska_red_all)  # Maska tylko dla koloru czerwonego
    cv2.imshow("Maska zielona", maska_ziel) # Maska tylko dla zielonego
    cv2.imshow("Maska zolty", maska_zolty) # Maska dla żółtego
    cv2.imshow("Maska pomarancz", maska_orange) #Maska dla pomaranczowego
    cv2.imshow("Maska bialego", maska_biala) #Maska dla bialego
    cv2.imshow("Maska niebieskiego", maska_nieb) #Maska dla niebieskiego


    # Wyświetlanie obrazu z nałożonym kwadratem ROI
    #cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)  # Zielony kwadrat ROI
    #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Zielony kwadrat ROI

    #cv2.imshow("Kamera", frame)  # Pełny obraz z konturami w ROI