## TEST #1 SZUKANIE KAMERY DROIDCAM 
## REZULTAT: SUKCES, KAMERE DROID CAM TRZEBA ZNALEZC ZA POMOCA IP W APLIKACJI WAZNE ABY TYLKO NA TEL JA MIEC ODPALONA
## UWAGI: PRZEZ USB NIE DZIALA MOZE WARTO BEDZIE ROZWAZYC ZAKUP INNEJ KAMERY W RAZIE PROBLEMÓW

import cv2
import numpy as np 

# for i in range(5):  # Testujemy kamery 0 i 1
#     cap = cv2.VideoCapture(i)
#     if cap.isOpened():
#         print(f"Testujemy kamerę {i}...")
#         ret, frame = cap.read()
#         if ret:
#             cv2.imshow(f"Kamera {i}", frame)
#             cv2.waitKey(2000)  # Podgląd przez 2 sekundy
#             cv2.destroyAllWindows()
#         else:
#             print(f"Kamera {i} nie zwraca obrazu.")
#         cap.release()


cap = cv2.VideoCapture("https://192.168.0.73:4343/video") ##MUSISZ MIEC DROIDCAMA ODPALONEGO NA TEL TYLKO
ret, frame = cap.read()
if ret:
    cv2.imshow("Kamera", frame)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
else:
    print("Kamera nie zwraca obrazu.")
cap.release()