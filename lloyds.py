"""
POKER BOT
skapad 21/11/2025
skapare Lloyd Björnstedt

Stegen 1-4 deklarerar funktioner
steg 1 - skapa kortlek + input från användaren och sparar datan + importerar itertools
steg 2 - kunna utvärdera olika kombinatioer
steg 3 - funktioner från steg 2 för att rangordna alla kombinationer
steg 4 - själva spelrundan
steg 5 - exikverar programmet
"""

# steg 1

from itertools import combinations
import random


# steg 2
def skapa_kortlek(lista,hk,cc):
    valör = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # alla valörer som tal
    färg = ["s", "k", "r", "h"]  # spader, klöver, ruter, hjärter (ÄNDRA SEN)

    for f in färg:
        for v in valör:
            lista.append(f + " " + str(v))

    for kort in hk+cc:
        lista.remove((kort))

    return lista

def kort_input(antal, numret, lista):
    for i in range(antal):  # antalet kort man ska dra
        färg, valör = input(f"kort {i + numret}: ").split(
            " ")  # Note to self: ValueError om inte split, (" ") för att garantera split

        # ger numeriskt värde till klädda kort
        if valör == "knäckt":
            valör = 11

        elif valör == "dam":
            valör = 12

        elif valör == "kung":
            valör = 13

        elif valör == "ess":
            valör = 14

        # färg + valör tillsammans
        lista.append(färg + " " + str(valör))



def bästa_kort(hand,x,stege,y,div):
    if stege:
        if sorted(hand) == [2,3,4,5,14]:
            return 0.05
        else:
            return (sorted(hand)[y])/100

    else:
        for kort in hand:
            if hand.count(kort) == x:
                return kort/div

# har par, tvåpar, triss, fyrtal eller färg = True
def par_triss_fyrtal_färg(antal, hand, tvåpar):
    if tvåpar:
        antal_par = 0

        for i in hand:
            if hand.count(i) == 2:
                antal_par += 1

        if antal_par == 4:  # count-funktionen har inte hänsyn till dubbletter
            return True

    else:
        for i in hand:
            if hand.count(i) == antal:
                return True

# har stege = True
def stege(hand):
    stegen = 1  # sparar antalet kort i direkt följd

    # ett kort med index "i" är kortet = förra kortet+1
    for i in range(1, len(hand)):
        if sorted(hand)[i] == sorted(hand)[i - 1] + 1:
            stegen += 1
        else:
            stegen = 1

    if stegen == 5:
        return True

    elif sorted(hand) == [2, 3, 4, 5, 14]:  # specialfallet då ess är lägsta kortet i en stege
        return True



def hand_eval(hand, rang):
    temp_valör = []
    temp_färg = []

    for kort in hand:
        färg, valör = kort.split(" ")

        temp_färg.append(färg)
        temp_valör.append(int(valör))

        # färgstege = 8
    if stege(temp_valör) and par_triss_fyrtal_färg(5, temp_färg, False):
        rang.append(8+bästa_kort(temp_valör,0, True,-1,100))
        return

        # fyrtal = 7
    elif par_triss_fyrtal_färg(4, temp_valör, False):
        rang.append(7+bästa_kort(temp_valör,4,False,0,100))
        return

        # kåk = 6
    elif par_triss_fyrtal_färg(2, temp_valör, False) and par_triss_fyrtal_färg(3, temp_valör, False):
            rang.append(6+bästa_kort(temp_valör, 3, False, 0,100) + bästa_kort(temp_valör, 2, False, 0,10000))
            return

        # färg = 5
    elif par_triss_fyrtal_färg(5, temp_färg, False):
        rang.append(5+bästa_kort(temp_valör, 0, True, -1,100))
        return

        # stege = 4
    elif stege(temp_valör):
        rang.append(4+bästa_kort(temp_valör, 0, True, -1,100))
        return

        # triss = 3
    elif par_triss_fyrtal_färg(3, temp_valör, False):
        rang.append(3+bästa_kort(temp_valör, 3, False, 0,100))
        return

        # tvåpar = 2
    elif par_triss_fyrtal_färg(2, temp_valör, True):
        rang.append(2+bästa_kort(temp_valör[::-1], 2, False, 0,100))
        return

        # par = 1
    elif par_triss_fyrtal_färg(2, temp_valör, False):
        rang.append(1+bästa_kort(temp_valör, 2, False, 0,100))
        return

        # högt kort/inget = 0
    else:
        rang.append(0+bästa_kort(temp_valör,0,stege,-1,100))
        return

def simulation(cc, hk, opps):
    sim = []
    self = []

    win = 0
    lose = 0
    tie = 0

    kl = []
    skapa_kortlek(kl, hk, cc)

    x = 5 - len(cc)

    for i in range(100):
        y = random.sample(kl, 2+x)

        for j in list(combinations(hk + cc + y[:x], 5)):  # min komb.
            hand_eval(j, self)

        for j in list(combinations(cc + y, 5)):  # simulerar möjliga komb.
            hand_eval(j, sim)

    for k in range(len(sim)):
        if len(hk + cc) == 7:
            if sim[k] < max(self):
                win += 1

            elif sim[k] > max(self):
                lose += 1
            else:
                tie += 1
        else:
            if sim[k] < self[k]:
                win += 1

            elif sim[k] > self[k]:
                lose += 1
            else:
                tie += 1

    print(win + tie + lose, len(kl))
    return f"win: {win:<7} tie: {tie:<7} lose: {lose:<7} %win: {round(((win + (0.5 * tie)) / (k)) * 100, 2):<8} \n"  # temp

def spelrunda():
    info_runda = ["Pre-flop", "Flop", "Turn", "River", 2, 3, 1, 1, 3, 6, 7]  # vilken runda (0-3) + antalet kort man drar (4-7) + numret på kortet (7-10)
    hålkort = []
    community_card = []

    for i in range(4):
        print("\n------------------------------------------")
        print(f"{info_runda[i]}\n\n")

        kort_input(info_runda[i + 4], info_runda[i + 7], hålkort)
        print(f"\n{simulation(community_card, hålkort,1)}")  # temp



# steg 3

#spelrunda()







hk = ["s 14", "k 14"]

cc1 = []                                        # pre flop
cc2 = ["k 10", "h 2", "h 5"]                    # flop
cc3 = ["k 10", "h 2", "h 5", "r 11"]            # turn
cc4 = ["k 10", "h 2", "h 5", "r 11", "r 4"]     # river

temp = [cc1, cc2, cc3, cc4]

for i in temp:
    print(simulation(i, hk, 0))

