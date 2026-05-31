import cv2
from kolory import wykryj
from roi import roi

def uruchom_kamere():

    cap = cv2.VideoCapture("https://192.168.0.73:4343/video")  # Używa kamerki (DroidCam na telefonie)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #wykryj(frame)  # Przetwarzanie obrazu

        pozycja = roi(frame)        #Pobranie pozycji ROI
        wykryj(frame, pozycja)      # Przetwarzanie obrazu z funkcją wykrywania kolorów


        cv2.imshow("Kamera", frame)          # Wyświetlanie klatki

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Wyjście po wciśnięciu 'q'
            break

    cap.release()
    cv2.destroyAllWindows()
