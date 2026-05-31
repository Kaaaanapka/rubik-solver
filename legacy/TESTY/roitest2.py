import cv2
import numpy as np

cap = cv2.VideoCapture("https://192.168.0.73:4343/video")  # Używa kamerki (DroidCam na telefonie)

def roi(frame):
    # PIERWSZA WARSTWA
    positions = [
        (240, 200), (290, 200), (340, 200),  # Góra
        (240, 250), (290, 250), (340, 250),  # Środek
        (240, 300), (290, 300), (340, 300)   # Dół
    ]
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Kolory dla warstw
    
    for i, (x, y) in enumerate(positions):
        cv2.rectangle(frame, (x, y), (x + 15, y + 15), colors[i // 3], 2)

    # # CAŁA KOSTKA
    # cv2.rectangle(frame, (150, 150), (450, 450), (255, 255, 255), 2)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie można pobrać obrazu z kamery.")
        break

    roi(frame)  # Narysowanie kwadratów na obrazie
    cv2.imshow('Obrazek', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Zatrzymanie pętli po naciśnięciu 'q'
        break

cap.release()  # Wyłącza kamerę
cv2.destroyAllWindows()  # Zamyka wszystkie okna
