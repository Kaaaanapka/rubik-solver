import cv2
import numpy as np

#Dostepne kolory
kolor_scianek = ['white', 'green', 'orange', 'red', 'blue', 'yellow']

#UKŁAD ŚCIAN KOSTKI GÓRNA LEWA PRAWA FRONT TYLNIA ETC
#      U
#    L F R B
#      D

mapowanie_kolorow = {
    'white': 'U',
    'red': 'R',
    'green': 'F',
    'yellow':'D',
    'orange': 'L',
    'blue': 'B'
}

kolory = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]  # Kolory dla warstw

def wykryj(frame, pozycja):
    # Iteracja po wszystkich kwadratach
    for i, (x, y) in enumerate(pozycja):
        # Rysowanie prostokątów wokół kwadratów
        cv2.rectangle(frame, (x, y), (x + 15, y + 15), kolory[i // 3], 2)

        # Wycinanie regionu ROI dla każdego kwadratu
        x_start = x
        x_end = x + 15
        y_start = y
        y_end = y + 15
        roi_1 = frame[y_start:y_end, x_start:x_end]

        # Konwersja ROI do przestrzeni HSV
        hsv = cv2.cvtColor(roi_1, cv2.COLOR_BGR2HSV)

        # Definicje kolorów w przestrzeni HSV
        dolny_red_1 = np.array([0, 100, 100])
        gorny_red_1 = np.array([5, 255, 255])

        dolny_red_2 = np.array([170, 100, 100])
        gorny_red_2 = np.array([179, 255, 255])

        dolny_ziel = np.array([45, 100, 100])
        gorny_ziel = np.array([85, 255, 255])

        dolny_zolty = np.array([25, 100, 100])
        gorny_zolty = np.array([32, 255, 255])

        dolny_orange = np.array([5, 100, 100])
        gorny_orange = np.array([20, 255, 255])

        dolny_bialy = np.array([0, 0, 200])
        gorny_bialy = np.array([180, 30, 255])

        dolny_nieb = np.array([90, 50, 50])
        gorny_nieb = np.array([130, 255, 255])

        # Tworzenie masek dla kolorów
        maska_red_1 = cv2.inRange(hsv, dolny_red_1, gorny_red_1)
        maska_red_2 = cv2.inRange(hsv, dolny_red_2, gorny_red_2)

        maska_ziel = cv2.inRange(hsv, dolny_ziel, gorny_ziel)
        maska_zolty = cv2.inRange(hsv, dolny_zolty, gorny_zolty)
        maska_orange = cv2.inRange(hsv, dolny_orange, gorny_orange)
        maska_biala = cv2.inRange(hsv, dolny_bialy, gorny_bialy)
        maska_nieb = cv2.inRange(hsv, dolny_nieb, gorny_nieb)

        # Łączenie masek
        maska_red_all = cv2.bitwise_or(maska_red_1, maska_red_2)
        maska_Red_Ziel = cv2.bitwise_or(maska_red_all, maska_ziel)
        maska_Zol_Ora = cv2.bitwise_or(maska_zolty, maska_orange)
        maska_RZZO = cv2.bitwise_or(maska_Red_Ziel, maska_Zol_Ora)
        maska_Bia_Nie = cv2.bitwise_or(maska_biala, maska_nieb)
        maska_all = cv2.bitwise_or(maska_RZZO, maska_Bia_Nie)

        # Detekcja kolorów w każdym z ROI
        if np.any(maska_red_all):
            cv2.putText(frame, "Czer!", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if np.any(maska_ziel):
            cv2.putText(frame, "Ziel!", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if np.any(maska_zolty):
            cv2.putText(frame, "Zolty!", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if np.any(maska_orange):
            cv2.putText(frame, "Pom!", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if np.any(maska_biala):
            cv2.putText(frame, "Bialy", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if np.any(maska_nieb):
            cv2.putText(frame, "Nieb", (x_start, y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Znajdowanie konturów w masce
            contours, _ = cv2.findContours(maska_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x + x_start, y + y_start), (x + x_start + w, y + y_start + h), (0, 0, 0), 2)

    # Wyświetlanie masek Debugowanie
    # cv2.imshow("Maska czerwonego", maska_red_all)
    # cv2.imshow("Maska zielona", maska_ziel)
    # cv2.imshow("Maska zolty", maska_zolty)
    # cv2.imshow("Maska pomarancz", maska_orange)
    # cv2.imshow("Maska bialego", maska_biala)
    # cv2.imshow("Maska niebieskiego", maska_nieb)
