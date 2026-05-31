import cv2
import numpy as np

# Wczytaj obraz

#image = cv2.imread('chonky_boi.png')

cap = cv2.VideoCapture("https://192.168.0.73:4343/video")  # Używa kamerki (DroidCam na telefonie)


def roi(frame):



    #PIERWSZA WARSTWA

    # Definicja pierwszego ROI (np. górna lewa część obrazu)
    x1, y1, w1, h1 = 190, 190, 20, 20  # (x, y, szerokość, wysokość)
    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)  # Zielony kwadrat

    # Definicja drugiego ROI (np. dolna prawa część obrazu)
    x2, y2, w2, h2 = 290, 190, 20, 20
    cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)  # Niebieski kwadrat

    # Definicja drugiego ROI (np. dolna prawa część obrazu)
    x3, y3, w3, h3 = 390, 190, 20, 20
    cv2.rectangle(frame, (x3, y3), (x3 + w3, y3 + h3), (255, 0, 0), 2)  # Niebieski kwadrat

    #DRUGA WARSTWA

    x4, y4, w4, h4 = 190, 290, 20, 20  # (x, y, szerokość, wysokość)
    cv2.rectangle(frame, (x4, y4), (x4 + w4, y4 + h4), (0, 255, 0), 2)  # Zielony kwadrat

    # Definicja drugiego ROI (np. dolna prawa część obrazu)
    x5, y5, w5, h5 = 290, 290, 20, 20
    cv2.rectangle(frame, (x5, y5), (x5 + w5, y5 + h5), (0, 255, 0), 2)  # Niebieski kwadrat

    # Definicja drugiego ROI (np. dolna prawa część obrazu)
    x6, y6, w6, h6 = 390, 290, 20, 20
    cv2.rectangle(frame, (x6, y6), (x6 + w6, y6 + h6), (0, 255, 0), 2)  # Niebieski kwadrat

    #TRZECIA WARSTWA

    x7, y7, w7, h7 = 190, 390, 20, 20  # (x, y, szerokość, wysokość)
    cv2.rectangle(frame, (x7, y7), (x7 + w7, y7 + h7), (0, 0, 255), 2)  # Zielony kwadrat

    # Definicja drugiego ROI (np. dolna prawa część obrazu)
    x8, y8, w8, h8 = 290, 390, 20, 20
    cv2.rectangle(frame, (x8, y8), (x8 + w8, y8 + h8), (0, 0, 255), 2)  # Niebieski kwadrat

    # Definicja drugiego ROI (np. dolna prawa część obrazu)
    x9, y9, w9, h9 = 390, 390, 20, 20
    cv2.rectangle(frame, (x9, y9), (x9 + w9, y9 + h9), (0, 0, 255), 2)  # Niebieski kwadrat


    #CALA KOSTKA 

    x0, y0, w0, h0 = 150, 150, 300, 300
    cv2.rectangle(frame, (x0, y0), (x0 + w0, y0 + h0), (255, 255,255), 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Wymiary obrazu
    height, width, _ = frame.shape

# Pokazanie wyciętych fragmentów

roi()

cv2.imshow('Obrazek', frame)


cap.release()  # Wyłącza kamerę
cv2.destroyAllWindows()  # Zamyka wszystkie okna
