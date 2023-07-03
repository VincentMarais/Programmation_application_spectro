from pyfirmata import Arduino, util

# remplacer 'COM3' par le port série correct de votre Arduino
board = Arduino('COM8')

it = util.Iterator(board)
it.start()
pin = board.get_pin('d:3:i')  # d pour digital, 3 pour le pin 3, i pour input

def fourche_optique_etat(pin):
        # définir le pin 3 comme entrée


    # une boucle pour lire l'état du pin
    state = pin.read()  # lire l'état du pin
            
    if state is not None:
            if state:
                        return 'Bonne photodiode'
            else:
                        return 'Mauvaise photodiode'
    else:
        return 'Le pin n\'est pas reconnu.'
    


a='0'
while a!='Bonne photodiode':
    L=[]
    j= 0
    while j < 4 :
        a=fourche_optique_etat(pin)
        L.append(a)
        j=len(L)
        print(L)
    print("Mauvaise photodiode")
    

print(fourche_optique_etat())