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

kort_lista = []

pf_rang = []
hand_rang = []



# steg 2

# tar input om kortets färg och valör
def kort_input(antal):
    for __ in range(antal):  # antalet kort man ska dra
        färg, valör = input(f"kort {len(kort_lista) + 1}: ").split(" ")  # ValueError om inte split, (" ") för att garantera split

        # ger numeriskt värde till klädda kort
        if valör == "knäckt":
            valör = 11

        elif valör == "dam":
            valör = 12

        elif valör == "kung":
            valör = 13

        elif valör == "ess":    # ess kan värderas som 1 och 14 i en stege
            valör = 14
            kort_lista.append(färg + " " + "1")

        # färg + valör tillsammans
        kort_lista.append(färg + " " + str(valör))



# handen har tvåpar = True
def tvåpar(hand):
    antal_par = 0

    for i in hand:
        if hand.count(i) == 2:
            antal_par += 1

    if antal_par == 4: # count-funktionen har inte hänsyn till dubbletter
        return True

# handen har par, triss, fyrtal eller färg = True
def par_triss_fyrtal_färg(antal, hand):
    for i in hand:
        if hand.count(i) == antal:
            return True

# handen har stege = True
def stege(hand):
    stegen = 1   # sparar antalet kort i direkt följd

    # för ett kort med index "i" är kort = förra kortet+1 (rekursivt)
    for i in range(1,len(hand)):
        if hand[i] == hand[i-1] + 1:
           stegen += 1
        else:
            stegen = 1

    if stegen == 5:
        return True



# ger ett numeriskt värde till hållkort kombinationer
def pre_flop_eval(hand, rang):
    temp_valör = []
    temp_färg = []

    for kort in hand:
        f, v = kort.split(" ")

        temp_färg.append(f)
        temp_valör.append(int(v))


    if par_triss_fyrtal_färg(2,temp_valör):
        rang.append(1)

    else:
        rang.append(0)

    return rang

# ger numeriskt värde till alla 5 kort kombinationer (0-8)
def hand_eval(hand, rang):
    temp_valör = []
    temp_färg = []

    for kort in hand:
        f, v = kort.split(" ")

        temp_färg.append(f)
        temp_valör.append(int(v))


    # färgstege = 8
    if stege(temp_valör) and par_triss_fyrtal_färg(5,temp_färg):
        rang.append(8)
        return rang

    # fyrtal = 7
    if par_triss_fyrtal_färg(4, temp_valör):
        rang.append(7)
        return rang

    # kåk = 6
    elif par_triss_fyrtal_färg(2, temp_valör) and par_triss_fyrtal_färg(3, temp_valör):
        rang.append(6)
        return rang

    # färg = 5
    elif par_triss_fyrtal_färg(5,temp_färg):
        rang.append(5)
        return rang

    # stege = 4
    elif stege(sorted(temp_valör)):
        rang.append(4)
        return rang

    # triss = 3
    elif par_triss_fyrtal_färg(3, temp_valör):
        rang.append(3)
        return rang

    # tvåpar = 2
    elif tvåpar(temp_valör):
        rang.append(2)
        return rang

    # par = 1
    elif par_triss_fyrtal_färg(2, temp_valör):
        rang.append(1)
        return rang

    # högt kort = 0
    else:
        rang.append(0)
        return rang

# berättar vad ens bästa hand är (tillfällig)
def hand(rang):
    bäst = sorted(rang)[-1] # tar fram den bästa handen (måste vara det sista elementet)

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
        return f"högt kort "



# själva spelet
def spelrunda():
    runda = ["Pre-flop","Flop","Turn","River",2,3,1,1]  # visa vilken runda + antalet kort man drar

    for i in range(4):
        print("\n------------------------------------------")
        print(f"{runda[i]}\n")
        kort_input(runda[i+4])
        print(" ")

        if i == 0:
            for hands in list(combinations(kort_lista,2)):
                pre_flop_eval(hands,pf_rang)

            print(hand(pf_rang))

        else:
            for hands in list(combinations(kort_lista,5)):
                hand_eval(hands,hand_rang)

            print(hand(hand_rang))

        print(len(hand_rang)+len(pf_rang))



# steg 3

spelrunda()
