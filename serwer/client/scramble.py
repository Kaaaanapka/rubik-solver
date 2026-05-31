import random

def generuj_scramble(dlugosc=19):
    #Zestaw ruchow
    ruchy = ['R', 'L', 'U', 'D', 'F', 'B']
    scramble = []
    modyfikatory = ['', '2', "'"]

    ostatni_ruch = None
    
    for _ in range(dlugosc):
        ruch = random.choice(ruchy)

        while ruch == ostatni_ruch:
            ruch = random.choice(ruchy)
        
        ruch += random.choice(modyfikatory)

        scramble.append(ruch)
        ostatni_ruch = ruch[0]            #zapamietuje ostatni ruch

    return " ".join(scramble)

