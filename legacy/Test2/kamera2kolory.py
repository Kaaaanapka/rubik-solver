import cv2
import numpy as np
#import roi() (testowanie czy roi.py działa)

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
    roi_size = 50  # Wielkość boku kwadratu w pikselach
    x_start = (width - roi_size) // 2  # Początek ROI (lewy górny róg)
    y_start = (height - roi_size) // 2  # Początek ROI (lewy górny róg)
    x_end = x_start + roi_size  # Koniec ROI (prawy dolny róg)
    y_end = y_start + roi_size  # Koniec ROI (prawy dolny róg)

# Liczba podzielonych kwadracików w poziomie i pionie

    num_rows = 3            #liczba wierszy
    num_cols = 3            #liczba kolumn

# Oblicz wymiary mniejszych kwadracików

    kwadracik_szer = roi_size // num_cols
    kwadracik_wys = roi_size // num_rows

# Przechodzimy przez każdy mniejszy kwadracik w regionie ROI

    for row in range(num_rows):
        for col in range(num_cols):
          # Obliczamy współrzędne lewego górnego i prawego dolnego rogu dla każdego kwadracika
          x1 = x_start + col * kwadracik_szer
          y1 = y_start + row * kwadracik_wys
          x2 = x1 + kwadracik_szer
          y2 = y1 + kwadracik_wys  

    # Wycinamy region ROI z obrazu
    roi = frame[y_start:y_end, x_start:x_end]

# # ========================================================= HSV

        # Przykładowe operacje na każdym małym kwadraciku
        # Konwersja do HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Możesz teraz używać tego małego regionu (roi_small) do dalszych operacji
        # np. maskowanie, detekcja kolorów itp.

        # Możesz również rysować prostokąty wokół tych małych kwadracików
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Zielony prostokąt

# ========================================================= KOLORY


    # Definicja kolorów kostki (dla koloru czerwonego)
    dolny_red_1 = np.array([0, 100, 100])  # Parametry HSV dolne dla koloru czerwonego
    gorny_red_1 = np.array([5, 255, 255])  # Parametry HSV górne

    dolny_red_2 = np.array([170, 100, 100])  # Parametry HSV dolne
    gorny_red_2 = np.array([179, 255, 255])  # Parametry HSV górne

    #Definicja kolorów kostki (dla koloru zielonego)

    dolny_ziel = np.array([45, 100, 100])      # Parametry HSV dolne zielony
    gorny_ziel = np.array([85, 255, 255])    # Parametry HSV górne zielony

    # dolny_ziel = np.array([35, 100, 50])      # Parametry HSV dolne zielony
    # gorny_ziel = np.array([85, 255, 255])    # Parametry HSV górne zielony

    #Definicja kolorow dla zoltego

    dolny_zolty = np.array([25, 100, 100])  # Dolne wartości dla koloru żółtego w HSV
    gorny_zolty = np.array([32, 255, 255])  # Górne wartości dla koloru żółtego w HSV
    # dolny_zolty = np.array([15, 100, 150])  # Dolne wartości dla koloru żółtego w HSV
    # gorny_zolty = np.array([45, 255, 255])  # Górne wartości dla koloru żółtego w HSV


    #Definicja HSV dla koloru pomarańczowego
    dolny_orange = np.array([10, 100, 100])  # Dolna granica (mocny pomarańczowy)
    gorny_orange = np.array([24, 255, 255])  # Górna granica (jasny pomarańczowy)

    #HSV dla białego

    dolny_bialy = np.array([0, 0 , 200])
    gorny_bialy = np.array([180, 30, 255])

    #HSV dla niebieskiego

    dolny_nieb = np.array([95, 100, 100])    # Dolny zakres (ciemniejszy niebieski)
    gorny_nieb = np.array([125, 255, 255])  # Górny zakres (jasny, nasycony niebieski)


    #ZROBIONE KOLORY (UWAGI)

    # CZERWONY [OK] 
    # ZIELONY [OK] 
    # ZOLTY [Przebija sie kolor pomaranczowy na 1/3] 
    # POMARANCZOWY [OK] 
    # BIAŁY [OK] 
    # NIEBIESKI [OK]                 
    #EWENTUALNA POPRAWA ZOLTEGO I ZIELONEGO TAK TO GIT RACZEJ JEST


    # Tworzenie masek dla koloru czerwonego
    maska_red_1 = cv2.inRange(hsv, dolny_red_1, gorny_red_1)
    maska_red_2 = cv2.inRange(hsv, dolny_red_2, gorny_red_2)

    #Tworzenie maski dla zielonego

    maska_ziel = cv2.inRange(hsv, dolny_ziel, gorny_ziel)

    #Tworzenie maski dla zoltego

    maska_zolty = cv2.inRange(hsv, dolny_zolty, gorny_zolty)

    #Maska dla pomarańczowego

    maska_orange = cv2.inRange(hsv, dolny_orange, gorny_orange)

    #Maska dla bialego

    maska_biala = cv2.inRange(hsv, dolny_bialy, gorny_bialy)

    #Maska dla niebieskiego

    maska_nieb = cv2.inRange(hsv, dolny_nieb, gorny_nieb)

#==========================================================================================

    # Łączenie masek czerwonych
    maska_red_all = cv2.bitwise_or(maska_red_1, maska_red_2)                    #polaczona maska_red_1 i maska_red_2 

    # Wycinamy maskę dla regionu ROI
    maska_Red_Ziel = cv2.bitwise_or(maska_red_all, maska_ziel)                   #cv2.bitwise_or przyjmuje tylko dwa argumenty dlatego je trzeba cześciami łaczyć
    maska_Zol_Ora = cv2.bitwise_or(maska_zolty, maska_orange)
    maska_RZZO = cv2.bitwise_or(maska_Red_Ziel, maska_Zol_Ora)                  #polaczenie masek Red_Ziel z Zol_Ora (bo tylko dwa parametry przyjmuje cv2.bitwise_or)

    maska_Bia_Nie = cv2.bitwise_or(maska_biala, maska_nieb)
    maska_all = cv2.bitwise_or(maska_RZZO, maska_Bia_Nie)


    # Sprawdzamy, czy w obrębie ROI znajduje się kolor dany kolor

    if np.any(maska_red_all[y_start:y_end, x_start:x_end]):  # Jeśli istnieją jakiekolwiek białe piksele w masce (czyli kolor czerwony jest obecny)
        cv2.putText(frame, "Czerwony!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
       
    elif np.any(maska_ziel[y_start:y_end, x_start:x_end]): 
        cv2.putText(frame, "Zielony!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
   
    elif np.any(maska_zolty[y_start:y_end, x_start:x_end]): 
        cv2.putText(frame, "Zolty!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
    elif np.any(maska_orange[y_start:y_end, x_start:x_end]):
        cv2.putText(frame, "Pomaranczowy!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 

    elif np.any(maska_biala[y_start:y_end, x_start:x_end]):
        cv2.putText(frame, "Bialy!", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 

    elif np.any(maska_nieb[y_start:y_end, x_start:x_end]):
        cv2.putText(frame, "Niebieski!", (70, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) 

        # Znajdowanie konturów w masce
        contours, _ = cv2.findContours(maska_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        # Rysowanie konturów na obrazie ROI
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filtrujemy małe kontury
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Rysowanie prostokąta

    # Wyświetlanie obrazu z nałożonym kwadratem ROI
    #cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)  # Zielony kwadrat ROI
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Zielony kwadrat ROI


    # Wyświetlanie wyników (przetworzony obraz i maska)
    cv2.imshow("Maska czerwonego", maska_red_all)  # Maska tylko dla koloru czerwonego
    cv2.imshow("Maska zielona", maska_ziel) # Maska tylko dla zielonego
    cv2.imshow("Maska zolty", maska_zolty) # Maska dla żółtego
    cv2.imshow("Maska pomarancz", maska_orange) #Maska dla pomaranczowego
    cv2.imshow("Maska bialego", maska_biala) #Maska dla bialego
    cv2.imshow("Maska niebieskiego", maska_nieb) #Maska dla niebieskiego
    cv2.imshow("Kamera", frame)  # Pełny obraz z konturami w ROI

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#roi() testowanie czy funkcja roi() z roi.py działa

cap.release()  # Wyłącza kamerę
cv2.destroyAllWindows()  # Zamyka wszystkie okna
