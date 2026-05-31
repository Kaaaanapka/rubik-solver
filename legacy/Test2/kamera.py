import cv2
import numpy as np

# ========================================================= ŁACZENIE KAMERKI

cap = cv2.VideoCapture("https://192.168.0.73:4343/video")  # Używa kamerki (DroidCam na telefonie)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Wymiary obrazu
    height, width, _ = frame.shape

# ========================================================= ROI

    # Definicja regionu ROI - kwadrat w centrum obrazu
    roi_size = 200  # Wielkość boku kwadratu w pikselach
    x_start = (width - roi_size) // 2  # Początek ROI (lewy górny róg)
    y_start = (height - roi_size) // 2  # Początek ROI (lewy górny róg)
    x_end = x_start + roi_size  # Koniec ROI (prawy dolny róg)
    y_end = y_start + roi_size  # Koniec ROI (prawy dolny róg)

    # Wycinamy region ROI z obrazu
    roi = frame[y_start:y_end, x_start:x_end]

# # ========================================================= HSV

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Konwersja z BGR na HSV

# ========================================================= KOLORY


    # Definicja kolorów kostki (dla koloru czerwonego)
    dolny_red_1 = np.array([0, 120, 70])  # Parametry HSV dolne dla koloru czerwonego
    gorny_red_1 = np.array([10, 255, 255])  # Parametry HSV górne

    dolny_red_2 = np.array([170, 120, 70])  # Parametry HSV dolne
    gorny_red_2 = np.array([180, 255, 255])  # Parametry HSV górne

    #Definicja kolorów kostki (dla koloru zielonego)

    dolny_ziel_1 = np.array([40, 100, 100])      # Parametry HSV dolne zielony
    gorny_ziel_1 = np.array([90, 255, 255])    # Parametry HSV górne zielony


    # Tworzenie masek dla koloru czerwonego
    maska_red_1 = cv2.inRange(hsv, dolny_red_1, gorny_red_1)
    maska_red_2 = cv2.inRange(hsv, dolny_red_2, gorny_red_2)

    maska_ziel_1 = cv2.inRange(hsv, dolny_ziel_1, gorny_ziel_1)

    # Łączenie masek
    maska_red_all = cv2.bitwise_or(maska_red_1, maska_red_2)                    #polaczona maska_red_1 i maska_red_2 

    # Wycinamy maskę dla regionu ROI
    maska_roi = maska_red_all[y_start:y_end, x_start:x_end]

    # Sprawdzamy, czy w obrębie ROI znajduje się kolor czerwony
    red_wykryty = False
    #ziel_wykryty = False
    if np.any(maska_roi):  # Jeśli istnieją jakiekolwiek białe piksele w masce (czyli kolor czerwony jest obecny)
        cv2.putText(frame, "Czerwony!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        #cv2.putText(frame, "Zielony!", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        red_wykryty = True
        #ziel_wykryty = True
        # Znajdowanie konturów w masce
        contours, _ = cv2.findContours(maska_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Rysowanie konturów na obrazie ROI
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filtrujemy małe kontury
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Rysowanie prostokąta

    # Wyświetlanie obrazu z nałożonym kwadratem ROI
    cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)  # Zielony kwadrat ROI

    # Wyświetlanie wyników (przetworzony obraz i maska)
    cv2.imshow("Maska Czerwonego", maska_red_all)  # Maska tylko dla koloru czerwonego
    cv2.imshow("Maska Zielona", maska_ziel_1) # Maska tylko dla zielonego
    cv2.imshow("Kamera", frame)  # Pełny obraz z konturami w ROI

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Wyłącza kamerę
cv2.destroyAllWindows()  # Zamyka wszystkie okna
