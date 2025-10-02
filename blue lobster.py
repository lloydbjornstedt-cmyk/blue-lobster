import random

player_1 = []
player_2 = []
player_3 = []
player_4 = []

alla_spelare = [player_1, player_2, player_3, player_4]

kortlek = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
           30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
           57, 58, 59, 60]
sakhög = []

alla_poäng = [0, 0, 0, 0]

wincon = 0

spelare_namn = input("Ange namn på alla spelare: ")
spelare_namn = spelare_namn.split(', ')

antal_spelare = len(spelare_namn)
aktiva_spelare = alla_spelare[:antal_spelare]
aktiva_poäng = alla_poäng[:antal_spelare]



def godkända_kort(spelare):
    sparade_kort = []
    kort = 1
    for j in range(0, 10):
        if kort <= spelare[j] <= kort + 5:
            sparade_kort.append(spelare[j])
        else:
            sparade_kort.append(False)
        kort += 6

    return sparade_kort

def god_kända_visa(spelare):
    sparade_kort = []
    kort = 1
    for j in range(0, 10):
        if kort <= spelare[j] <= kort + 5:
            print(j + 1, ": Godkänt")
        else:
            print(j + 1, ": Icke godkänd")
        kort += 6

    return sparade_kort

def Adjust_Interval(approved_cards):
    approved_cards_stripped = []
    intervals = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
    min_val = 1
    max_val = 60
    for approved_card in approved_cards:
        if approved_card != False:
            if approved_card == approved_cards[0]:
                min_val = approved_card
            if approved_card == approved_cards[-1]:
                max_val = approved_card
            else:
                approved_cards_stripped.append(approved_card)

    for card in approved_cards_stripped:
        intervals[approved_cards.index(card)] = card
        length = approved_cards.index(card)
        position = approved_cards.index(card)
        prev_card = approved_cards_stripped[approved_cards_stripped.index(card) - 1]
        prev_length = approved_cards.index(prev_card)
        if card == approved_cards_stripped[0]:
            for interval in range(position):
                range_val = card - min_val
                jump = int(round(range_val / length))
                intervals[interval] = (min_val - 1) + jump
                min_val += jump
                length -= 1
        else:
            for interval in range(position - prev_length - 1):
                range_val = card - min_val - 1
                jump = int(round(range_val / (length - prev_length - 1)))
                intervals[prev_length + 1 + interval] = min_val + jump
                min_val += jump + 1
                length -= 1
        if card == approved_cards_stripped[-1]:
            length = approved_cards.index(card)
            card = max_val
            intervals[-1] = card
            for interval in range(9 - position):
                range_val = card - min_val
                jump = int(round(range_val / (9 - length)))
                intervals[position + 1 + interval] = min_val + jump
                min_val += jump + 1
                length += 1

    return intervals

def kortcheck(intervals,kort):
    rätt_plats = []
    for j in range(0,9):
        if intervals[j] < kort <= intervals[j+1]:
            #if intervals[j+1] != False:
            rätt_plats.append(j+2)
        #if len(rätt_plats)==0:
            #return "ta från kortleken"
    return kort,"passar i",rätt_plats[-1]

def blanda_kort(hög):
    random.shuffle(hög)
    return hög


def visa_kort(hand):
    for kort in hand:
        print(hand.index(kort) + 1, ":", kort)


def kortutdelning(alla_spelare, lek, sakhög):
    blanda_kort(lek)
    for spelare in alla_spelare:
        for _ in range(10):
            kort = lek.pop(0)
            spelare.append(kort)
    sakhög.append(lek.pop(0))
    return alla_spelare


# fixa så att första kortet i kortleken efter utdelning hamnar i sakhögen

def poäng_bricka(spelare):
    poäng = 5
    for i in range(0, 9):
        if spelare[i] < spelare[i + 1]:
            poäng += 5
        elif spelare[i] > spelare[i + 1]:
            break
    return poäng


def Special_Racko(x):
    if x > 6:
        x = 6
    bonuspoäng = 50 * (2 ** (x - 3))
    return bonuspoäng
    # failsafehantering är att 3 <= x <= 6


def Räkna_Poäng(aktiva_poäng, spelare, aktiva_spelare):
    for tur in range(len(aktiva_spelare)):
        #separat för spelaren som vann:
        poäng = aktiva_poäng[tur]
        if aktiva_spelare[tur] == spelare:
            poäng += 25
            count = 1
            consecutive_runs_list = []
            for i in range(9):
                if spelare[i + 1] == spelare[i] + 1:
                    count += 1
                else:
                    consecutive_runs_list.append(count)
                    count = 1
            highest_consecutive = max(consecutive_runs_list)
            if highest_consecutive >= 3:
                poäng += Special_Racko(highest_consecutive)
        print(spelare_namn[tur])
        poäng += poäng_bricka(aktiva_spelare[tur])
        print("Poäng: ", poäng)
        aktiva_poäng[tur] = poäng


def spelrunda(spelare, kortlek, sakhög):
    poäng_bricka(spelare)
    god_kända_visa(aktiva_spelare[tur])
    print(Adjust_Interval(godkända_kort(aktiva_spelare[tur])))
    print(kortcheck(Adjust_Interval(Adjust_Interval(godkända_kort(aktiva_spelare[tur]))), sakhög[-1]))
    print("")
    visa_kort(spelare)
    print("Sakhög:", sakhög[-1])

    val = (input("Ta upp? ja/nej: "))
    if val == "ja" or val == "Ja":
        byta = int(input("Byta (index): "))
        spelare.insert(byta - 1, sakhög.pop(-1))
        sakhög.append(spelare.pop(byta))
        visa_kort(spelare)
        print("\n\n")


    elif val == "nej" or val == "Nej":
        print(kortcheck(Adjust_Interval(Adjust_Interval(godkända_kort(aktiva_spelare[tur]))), kortlek[0]))
        print("\n")
        print("Kortlek:", kortlek[0], " ", "Sakhög:", sakhög[-1])
        # Behövs sakhögen också printas ut? man kommer ju inte kunna komma åt det/ ta upp det ändå
        val = (input("Behålla ja/nej: "))

        if val == "ja" or val == "Ja":
            byta = int(input("Byta (index): "))
            spelare.insert(byta - 1, kortlek.pop(0))
            sakhög.append(spelare.pop(byta))
            print(visa_kort(spelare), "\n", "\n")
            print("")

        elif val == "nej" or val == "Nej":
            sakhög.append(kortlek.pop(0))
            print("")



"""
def bot1():
    print("bot1")

def bot2():
    print("bot2")
"""

aktiva_spelare = kortutdelning(aktiva_spelare, kortlek, sakhög)
while 500 not in aktiva_poäng:
    while wincon < 1:
        for tur in range(0, antal_spelare):
            print(spelare_namn[tur], "'s tur", sep='')
            spelrunda(aktiva_spelare[tur], kortlek, sakhög)
            if aktiva_spelare[tur] == sorted(aktiva_spelare[tur]):
                svar = input("Du har Rack-o! \n\nVill du fortsätta?\n")
                if svar == "nej" or svar == "Nej":
                    print(aktiva_spelare[tur])
                    print("\nRundan har avslutats då", spelare_namn[tur],
                          "har fått Rack-o!\n\nHär är den nuvarande poängställningen:")
                    Räkna_Poäng(aktiva_poäng, aktiva_spelare[tur], aktiva_spelare)
                    # vinnare = alla_poäng.index(max(alla_poäng))
                    # print("\nDetta betyder att", spelare_namn[vinnare], "har vunnit!")
                    wincon += 1
                    break

# Rack-o 75p
# 3kort = 50p
# 4kort = 100p
# 5kort = 200p
# 6kort = 400p

# f(3) = 50
# f(4) = 100
# f(5) = 200
# f(6) = 400

# f(x) = 50*2**(x-3)