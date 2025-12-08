
"""
POKER BOT
skapad 21/11/2025
skapare Lloyd Björnstedt
senaste uppdatering:

steg 1
steg 2
steg 3

"""

# steg 1
from itertools import combinations

färg_list = []
valör_list = []
hand_rang = []
kort_lista = []



# steg 2

# tar input om kortets färg och valör
def player_input():
    kort = input(f"kort {len(valör_list) + 1}: ")
    kort_lista.append(kort) # valör och färg tillsammans för färgstege

    färg, valör = kort.split()  # ValueError om inte split

    # ger numeriskt värde till klädda kort
    if valör == "knäckt":
        valör = 11

    elif valör == "dam":
        valör = 12

    elif valör == "kung":
        valör = 13

    elif valör == "ess":
        valör = 14
        valör_list.append(1)    # ess kan värderas som mista och största kortet i en stege (ess = 14)

    # färg och valör separat
    färg_list.append(färg)
    valör_list.append(int(valör))   #sparar valörer som int för enklare värdering



# ger kortet med högst numeriskt värde
def high_card(lista):
    if sorted(lista)[-1] == 14:
        hc = "ess"

    elif sorted(lista)[-1] == 13:
        hc = "kung"

    elif sorted(lista)[-1] == 12:
        hc = "dam"

    elif sorted(lista)[-1] == 11:
        hc = "knäckt"

    elif sorted(lista)[-1] == 10:
        hc = 10

    else:
        hc = int(sorted(lista)[-1])

    return hc

# handen har tvåpar = True
def tvåpar(lista):
    antal_par = 0

    for i in lista:
        if lista.count(i) == 2:
            antal_par += 1

    if antal_par == 4: # count-funktionen har inte hänsyn till dubbletter
        return True

# handen har par, triss, fyrtal eller färg = True
def par_triss_fyrtal_färg(antal, lista):
    for i in lista:
        if lista.count(i) == antal:
            return True

# handen har stege = True
def stege(lista):
    stege = 1   # sparar antalet kort i direkt följd

    # för ett kort med index "i" är kort = förra kortet+1 (rekursivt)
    for i in range(len(lista)):
        if lista[i] == lista[i-1] + 1:
           stege += 1
        else:
            stege = 1

    if stege == 5:
        return True

# handen har färgsteg = True
def färgsteg(lista):
    for hand in lista:
        temp_valör = []
        temp_färg = []

        for kort in hand:
            f, v = kort.split()

            if v == "knäckt":
                v = 11

            elif v == "dam":
                v = 12

            elif v == "kung":
                v = 13

            elif v == "ess":
                v = 14

            temp_färg.append(f)
            temp_valör.append(int(v))

        if stege(sorted(temp_valör)) and par_triss_fyrtal_färg(5,temp_färg):
            return True



# ger ett numeriskt värde till alla hållkort kombinationer
def pre_flop_eval(hand,rang):
    if par_triss_fyrtal_färg(2,hand):
        rang.append(1)
    else:
        return rang.append(0)

# ger numeriskt värde till alla möjliga 5 kort kombinationer (0-8)
def hand_eval(alla_komb,rang):
    for hand in alla_komb:
        # färgstege = 8
        if färgsteg(list(combinations(kort_lista,5))):
            rang.append(8)

        # fyrtal = 7
        if par_triss_fyrtal_färg(4, hand):
            rang.append(7)

        # kåk = 6
        elif par_triss_fyrtal_färg(2, hand) and par_triss_fyrtal_färg(3, hand):
            rang.append(6)

        # färg = 5
        elif par_triss_fyrtal_färg(5,färg_list):
            rang.append(5)

        # stege = 4
        elif stege(sorted(hand)):
            rang.append(4)

        # triss = 3
        elif par_triss_fyrtal_färg(3, hand):
            rang.append(3)

        # tvåpar = 2
        elif tvåpar(hand):
            rang.append(2)

        # par = 1
        elif par_triss_fyrtal_färg(2, hand):
            rang.append(1)

        # högt kort = 0
        else:
            rang.append(0)

    return rang

# berättar vad ens bästa hand är (tillfällig)
def hand(bäst):
    bäst = sorted(bäst)[-1] # tar fram den bästa handen (måste vara det sista elementet)

    # utvärderar vad den bästa handen är
    if bäst == 8:
        return "färgstege"

    elif bäst == 7:
        return "fyrtal"

    elif bäst == 6:
        return "kåk"

    elif bäst == 5:
        return "färg"

    elif bäst == 4:
        return "stege"

    elif bäst == 3:
        return "triss"

    elif bäst == 2:
        return "tvåpar"

    elif bäst == 1:
        return "par"

    elif bäst == 0:
        return f"högt kort ({high_card(valör_list)})"


"""
# steg 3
print("------------------------------------------")
print("Pre-game info\n")

sb = int(input("small blind: "))
bb = int(input("big blind: "))
start_marker = int(input("antal marker vid start: "))
spelare = int(input("antal spelare: "))
plats = int(input("platser från dealer: "))



spelare_marker = []
for i in range(spelare):
    spelare_marker.append(start_marker)

print(spelare_marker)

print("\n------------------------------------------")

"""





print("Pre-flop\n")
for i in range(2):
    player_input()

pre_flop_eval(valör_list,hand_rang)
print(hand(hand_rang))
print("\n------------------------------------------")



print("Flop\n")
for i in range(3):
    player_input()

hand_eval(list(combinations(valör_list,5)),hand_rang)
print(hand(hand_rang))
print("\n------------------------------------------")



print("Turn\n")
player_input()

hand_eval(list(combinations(valör_list,5)),hand_rang)
print(hand(hand_rang))
print("\n------------------------------------------")



print("River\n")
player_input()

hand_eval(list(combinations(valör_list,5)),hand_rang)
print(hand(hand_rang))
print("\n------------------------------------------\n")



