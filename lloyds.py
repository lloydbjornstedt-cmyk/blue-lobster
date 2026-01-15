"""
POKER BOT
skapad: 21/11/2025
skapare: Lloyd Björnstedt

Ett programm som ska fatta beslut åt användaren i spelet Texas hold'em

Stegen 1-4 deklarerar funktioner
steg 1 - skapa kortlek + input från användaren och sparar datan + importerar itertools
steg 2 - kunna utvärdera olika kombinatioer
steg 3 - funktioner från steg 2 för att rangordna alla kombinationer
steg 4 - själva spelrundan
steg 5 - exikverar
"""

from itertools import combinations as comb
import random


# skapar en kortlek
def skapa_kortlek(lista, kända_kort):
    valör = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]  # alla valörer som tal
    färg = ["s", "k", "r", "h"]  # spader, klöver, ruter, hjärter (ÄNDRA SEN)

    for f in färg:
        for v in valör:
            lista.append(f + " " + v)

    for kort in kända_kort:
        lista.remove((kort))

    return lista

# tar input från användaren
def kort_input(antal, num_kort, lista):
    for i in range(antal):  # antalet kort man ska dra
        färg, valör = input(f"kort {i + num_kort}: ").split(" ")  # Note to self: ValueError om inte split, (" ") för att garantera split

        # ger numeriskt värde till klädda kort
        if valör == "knäckt":
            valör = "11"

        elif valör == "dam":
            valör = "12"

        elif valör == "kung":
            valör = "13"

        elif valör == "ess":
            valör = "14"

        lista.append(färg + " " + valör)  # färg + valör = hela kortet



# bestämmer bästa kortet i kombinationen
def bästa_kort(hand, stege=False, div=100, antal=0):
    if stege:
        if sorted(hand) == [2, 3, 4, 5, 14]:
            return 0.05
        else:
            return (sorted(hand)[-1])/100

    else:
        for kort in hand:
            if hand.count(kort) == antal:
                return kort/div

# har par, tvåpar, triss, fyrtal eller färg -> True
def par_triss_fyrtal_färg(antal, hand, tvåpar=False):
    if tvåpar:
        antal_par = 0

        for kort in hand:
            if hand.count(kort) == 2:
                antal_par += 1

        if antal_par == 4:  # count-funktionen har inte hänsyn till dubbletter
            return True

    else:
        for kort in hand:
            if hand.count(kort) == antal:
                return True

# har stege -> True
def stege(hand):
    stegen = 1  # sparar antalet kort i direkt följd

    # kort med index "i" är kortet = förra kortet+1
    for i in range(1, len(hand)):
        if sorted(hand)[i] == sorted(hand)[i - 1] + 1:
            stegen += 1
        else:
            stegen = 1

    if stegen == 5:
        return True

    elif sorted(hand) == [2, 3, 4, 5, 14]:  # specialfallet då ess är lägsta kortet i en stege
        return True



# utvärderar hand med 5 kort
def hand_eval(hand, rang):
    temp_valör = []
    temp_färg = []

    for kort in hand:
        färg, valör = kort.split(" ")

        temp_färg.append(färg)
        temp_valör.append(int(valör))

    # färgstege = 8
    if stege(temp_valör) and par_triss_fyrtal_färg(5, temp_färg):
        rang.append(8 + bästa_kort(temp_valör, stege=True))
        return

    # fyrtal = 7
    elif par_triss_fyrtal_färg(4, temp_valör, False):
        rang.append(7 + bästa_kort(temp_valör, antal=4))
        return

    # kåk = 6
    elif par_triss_fyrtal_färg(2, temp_valör) and par_triss_fyrtal_färg(3, temp_valör):
        rang.append(6 + bästa_kort(temp_valör, antal=3) + bästa_kort(temp_valör, antal=2, div=10000))
        return

    # färg = 5
    elif par_triss_fyrtal_färg(5, temp_färg):
        rang.append(5 + bästa_kort(temp_valör, stege=True))
        return

    # stege = 4
    elif stege(temp_valör):
        rang.append(4 + bästa_kort(temp_valör, stege=True))
        return

    # triss = 3
    elif par_triss_fyrtal_färg(3, temp_valör):
        rang.append(3 + bästa_kort(temp_valör, antal=3))
        return

    # tvåpar = 2
    elif par_triss_fyrtal_färg(2, temp_valör, True):
        rang.append(2 + bästa_kort(temp_valör[::-1], antal=2) + bästa_kort(sorted(temp_valör), antal=2, div=10000))
        return

    # par = 1
    elif par_triss_fyrtal_färg(2, temp_valör):
        rang.append(1 + bästa_kort(temp_valör, antal=2))
        return

    # högt kort/inget = 0
    else:
        rang.append(0 + bästa_kort(temp_valör, stege=True))
        return

# bestämmer sannolikhet för vinst
def simulering(cc, hk, iter=100):
    sim = []
    self = []
    kortlek = []
    win = lose = tie = 0

    skapa_kortlek(kortlek, hk + cc)
    x = 5 - len(cc)

    komb = list(comb(kortlek,2))

    for __ in range(iter):
        for i in komb:
            kortlek.clear()
            skapa_kortlek(kortlek, hk + cc + list(i))
            y = random.sample(kortlek, 5)

            for j in list(comb(hk + cc + y[:x], 5)):  # min komb.
                hand_eval(j, self)

            for j in list(comb(list(i) + cc + y[:x], 5)):  # simulerar möjliga komb.
                hand_eval(j, sim)

    bäst = max(self)
    for self1, sim1 in zip(self, sim):
        if len(hk + cc) == 7:
            if sim1 < bäst:
                win += 1

            elif sim1 > bäst:
                lose += 1

            else:
                tie += 1
        else:
            if sim1 < self1:
                win += 1

            elif sim1 > self1:
                lose += 1

            else:
                tie += 1

    print(win + tie + lose, len(kortlek))  # temp
    return f"win: {win:<7} tie: {tie:<7} lose: {lose:<7} %win: {((win + (0.5 * tie)) / (win + tie + lose)) * 100:.2f} \n"  # temp

# själva spelrundan
def spelrunda():
    info = {"Pre-flop": 2, "Flop": 3, "Turn": 1, "River": 1}

    hålkort = []
    community_cards = []

    for runda, antal_kort in info.items():
        print(f"\n------------------------------------------\n{runda}\n\n")

        if runda == "Pre-flop":
            kort_input(antal_kort, len(hålkort + community_cards) + 1, hålkort)
            print(f"\n{simulering(community_cards, hålkort, 500)}")

        else:
            kort_input(antal_kort, len(hålkort + community_cards) + 1, community_cards)
            print(f"\n{simulering(community_cards, hålkort, 500)}")


#spelrunda()


def beslut():
    pass


hk = ["k 14", "r 14"]

cc1 = []                                        # pre flop
cc2 = ["h 7", "h 11", "r 4"]                   # flop
cc3 = ["h 7", "h 11", "r 4", "k 2"]            # turn
cc4 = ["h 7", "h 11", "r 4", "k 2", "s 7"]     # river

temp = [cc1, cc2, cc3, cc4]

for i in temp:
    print(simulering(i, hk, 1))
