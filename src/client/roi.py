
import cv2
import numpy as np

def roi(frame):
    # PARAMETRY

    x1, x2, x3, x4, x5, x6, x7, x8, x9 = 250, 300, 350, 250, 300, 350, 250, 300 ,350
    y1, y2, y3, y4, y5, y6, y7, y8, y9 = 200, 200, 200, 250, 250, 250, 300, 300, 300

    pozycja = [
        (x1, y1), (x2, y2), (x3, y3),  # Góra
        (x4, y4), (x5, y5), (x6, y6),  # Środek
        (x7, y7), (x8, y8), (x9, y9)   # Dół
    ]

    return pozycja


    # kolory = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]  # Kolory dla warstw
    
    # # for i, (x, y) in enumerate(pozycja):
    # #     cv2.rectangle(frame, (x, y), (x + 15, y + 15), kolory[i // 3], 2)

    # # CAŁA KOSTKA
    # cv2.rectangle(frame, (150, 150), (450, 450), (255, 255, 255), 2)

