"""
------------------------------------------------------------------------------
POKER BOT
Skapad: 2025-11-21
Skapare: Lloyd Björnstedt

Ett program som ska fatta beslut åt användaren i spelet "Texas hold'em" baserat på korten som tilldelas

(Stegen 1-4 deklarerar funktioner)
STEG 1* - skapa kortlek + input från användaren (sparar korten) + importerar itertools och random
STEG 2  - kunna utvärdera alla kombinatioer
STEG 3* - avgör bästa 5-kort handen + bästa kortet i kombinationen
STEG 4* - själva spelrundan + funktionen som säger vad spelaren ska göra
STEG 5  - återkallar spelrunda-fumktionen (spelar spelet på riktigt)

* Hur nödvändig information om ett kort sparas (STEG 1)
Alla kort sparas som en sträng där färgen förkortas till första bokstaven och valören ges ett numeriskt värde

* Hur 5-kort händer rangordnas (STEG 3)
Varje hand blir tilldelad ett decimaltal i funktionen "hand_eval" som sedan kan jämföras.
Heltalssiffran motsvarar den huvudsakliga kombinationen och decimalerna motsvarar vilket det bästa kortet i kombinationen är.
Exempelvis är 2.09 par i 9:or, 2 är för par och 0.09 är kortet som är i par. Mer information står i hand_eval funktionen.
Notera att kåk och tvåpar har fler decimaler för att representera styrkan av båda kombinationer (triss + par eller par + par).

* Beslutsfattningsmodellen (STEG 4)
Modellen baseras på standard poker-teori med koncept som "pot equity", "pot odds" och "expected value (ev)".
Viss information ges men i koden men läsaren kan behöva söka upp mer informaion om ämnet.
------------------------------------------------------------------------------
"""

# ------- STEG 1 -------

from itertools import combinations as comb
from functools import lru_cache as cache
from collections import Counter
import random
import time  # start = time.perf_counter() # stop = time.perf_counter()

hash_lookup = {}

# skapar en kortlek
def skapa_kortlek(kända_kort=None):
    if kända_kort is None:
        kända_kort = []
    färg = ["s", "k", "r", "h"]  # spader, klöver, ruter, hjärter (ÄNDRA SEN)

    # skapar listan och tar bort reda kända kort
    lista = [(f, v) for f in färg for v in range(2, 15) if (f, v) not in kända_kort]

    return lista

# tar input från användaren
def kort_input(antal_kort, num_kort, lista):
    for i in range(antal_kort):  # antalet kort man ska dra
        färg, valör = input(f"kort {i + num_kort}: ").lower().split(
            " ")  # .lower() ifall användaren skriver med stora bokstäver
        # Note to self: ValueError om inte split, (" ") för att garantera split

        # ger numeriskt värde till klädda kort
        if valör == "knäckt":
            valör = 11

        elif valör == "dam":
            valör = 12

        elif valör == "kung":
            valör = 13

        elif valör == "ess":
            valör = 14

        tuple_kort = (färg, valör)
        lista.append(tuple_kort)

    # skapar en hash-nyckel för varje kort

# skapar hash-nyckel för en 5-kort hand
def hash_funktion(hand):
    primtal = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    prim_hash = 1
    flush = True
    färg = hand[0][0]

    for f, v in hand:
        prim_hash *= primtal[v - 2]
        if f != färg:
            flush = False

    if flush:
        prim_hash *= 43

    return prim_hash



# ------- STEG 2 -------

# bestämmer bästa kortet i kombinationen
def bästa_kort(hand, komb):

    temp_dict = Counter(hand)
    score = 0

    temp_hand = []

    for kort in hand:
        if kort not in temp_hand:
            temp_hand.append(kort)

    if komb == "stege": # stege ger det bästa kortet i handen (används mer än bara för stege)
        if hand == [2, 3, 4, 5, 14]:  # specialfall då ess = 1
            hand.remove(14)           # ess är inte det bästa kortet i detta fall

        return (hand[-1] * 10_000) + (hand[-2] * 100) + (hand[-3])

    elif komb == "kåk":
        for val, ant in temp_dict.items():
            if ant == 3:
                score += (val*10_000)

            elif ant == 2:
                score += (val*100)

        return score

    elif komb == "fyrtal":
        for val, ant in temp_dict.items():
            if ant == 4:
                score += (val * 10_000)

            elif ant == 1:
                score += (val * 100)

        return score

    elif komb == "tvåpar":
        tvåpar = []
        for val, ant in temp_dict.items():
            if ant == 2:
                tvåpar.append(val)
                temp_hand.remove(val)

        sort_tvåpar = sorted(tvåpar)
        return (sort_tvåpar[1] * 10_000) + (sort_tvåpar[0]*100) + temp_hand[-1]

    elif komb == "par":
        for val, ant in temp_dict.items():
            if ant == 2:
                score += (val * 10_000)
                temp_hand.remove(val)

        return score + (temp_hand[-1] * 100) + (temp_hand[-2])

    return 0

# har par, tvåpar, triss, fyrtal eller färg -> True
def par_triss_fyrtal_färg(hand, antal, tvåpar=False):
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

    return False

# har stege -> True
def stege(hand):
    stegen = 1  # sparar antalet kort i direkt följd

    # kort med index "i" är kortet = förra kortet+1
    for i in range(1, 5):
        if hand[i] == hand[i - 1] + 1:
            stegen += 1

    if stegen == 5:
        return True

    elif hand == [2, 3, 4, 5, 14]:  # specialfallet då ess är lägsta kortet i en stege
        return True

    return False



# ------- STEG 3 -------

# utvärderar hand med 5 kort
def hand_eval(hand):
    temp_valör = []
    temp_färg = []

    for kort in hand:
        färg, valör = kort

        temp_färg.append(färg)
        temp_valör.append(valör)

    sort_valör = sorted(temp_valör)

    # färgstege = 8
    if stege(sort_valör) and par_triss_fyrtal_färg(temp_färg, 5):
        return (8_000_000 + bästa_kort(sort_valör, "stege"))

    # fyrtal = 7
    elif par_triss_fyrtal_färg(temp_valör, 4):
        return (7_000_000 + bästa_kort(sort_valör, "fyrtal"))

    # kåk = 6
    elif par_triss_fyrtal_färg(temp_valör, 2) and par_triss_fyrtal_färg(temp_valör, 3):
        return (6_000_000 + bästa_kort(temp_valör, "kåk"))

    # färg = 5
    elif par_triss_fyrtal_färg(temp_färg, 5):
        return (5_000_000 + bästa_kort(sort_valör, "stege"))

    # stege = 4
    elif stege(sort_valör):
        return (4_000_000 + bästa_kort(sort_valör, "stege"))

    # triss = 3
    elif par_triss_fyrtal_färg(temp_valör, 3):
        return (3_000_000 + bästa_kort(temp_valör, "triss"))

    # tvåpar = 2
    elif par_triss_fyrtal_färg(temp_valör, 2, True):
        return (2_000_000 + bästa_kort(sort_valör, "tvåpar"))

    # par = 1
    elif par_triss_fyrtal_färg(temp_valör, 2):
        return (1_000_000 + bästa_kort(temp_valör, "par"))

    # högt kort/inget = 0
    else:
        return (0 + bästa_kort(sort_valör, "stege"))

@cache(maxsize=300_000)
def hash_eval(hand):
    key = hash_funktion(hand)
    return hash_lookup[key]

# bestämmer sannolikhet för vinst
def simulering(cc, hk, iter):
    win = tie = 0
    kortlek = skapa_kortlek(hk + cc)
    kort_kvar = 5 - len(cc)  # antalet kort som ska ut på bordet

    for __ in range(iter):
        urval_kort = random.sample(kortlek, kort_kvar + 2)
        bord = cc + urval_kort[:kort_kvar]
        opp_hk = urval_kort[kort_kvar:]

        p1 = max([hash_eval(i) for i in comb(hk + bord, 5)])
        p2 = max([hash_eval(i) for i in comb(opp_hk + bord, 5)])

        if p2 < p1:
            win += 1

        elif p2 == p1:
            tie += 1

    equity = (win + (0.5 * tie)) / iter

    print(len(kortlek), iter)
    print(f"win: {win:<7} tie: {tie:<7} lose: {(iter) - (win + tie):<7} %win: {100 * equity:.2f}")
    return equity



# ------- STEG 4 -------

# säger vad spelaren ska göra
def beslut(win_chans):
    call = int(input(f"syna: "))
    pot = int(input(f"pot: "))

    odds = call / (pot + call)

    if win_chans >= odds:
        print("call")
        print(f"{100 * odds:.2f} | {100 * win_chans}")
    else:
        print("fold")
        print(f"{100 * odds:.2f} | {100 * win_chans}")

# själva spelrundan
def spelrunda():
    hålkort = []
    community_cards = []
    info = {"Pre-flop": (1, 2, hålkort), "Flop": (2, 3, community_cards), "Turn": (5, 1, community_cards),
            "River": (6, 1, community_cards)}

    for runda, kort in info.items():
        kort_num, kort_antal, kort_lista = kort

        print(f"\n------------------------------------------\n{runda}\n\n")
        kort_input(kort_antal, kort_num, kort_lista)

        x = simulering(community_cards, hålkort, 1000)
        beslut(x)



# ------- STEG 5 -------

# spelrunda()


hk = [("h", 14), ("s", 10)]

cc1 = []
cc2 = [("k", 6), ("s", 7), ("k", 13)]
cc3 = [("k", 6), ("s", 7), ("k", 13), ("s", 11)]
cc4 = [("k", 6), ("s", 7), ("k", 13), ("s", 11), ("r", 7)]

temp = [cc1, cc2, cc3, cc4]

start1 = time.perf_counter()
kl = skapa_kortlek()
for i in comb(kl, 5):
    x = hash_funktion(i)
    if x not in hash_lookup:
        hash_lookup[x] = hand_eval(i)
stop1 = time.perf_counter()
print(len(hash_lookup))
print(f"{stop1 - start1:.4f}\n")

for i in temp:
    start = time.perf_counter()
    simulering(i, hk, 10_000)
    print(hash_eval.cache_info())
    stop = time.perf_counter()
    print(f"{stop - start:.4f}\n")