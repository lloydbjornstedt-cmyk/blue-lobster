# -----------------------
# VARIABLER och LISTOR
# -----------------------


import random

kortlek = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
           30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
           57, 58, 59, 60]

sakhög = []

alla_poäng = [0, 0, 0, 0]

wincon = 0

player_1 = []
player_2 = []
player_3 = []
player_4 = []

alla_spelare = [player_1, player_2, player_3, player_4]

spelare_namn = input("Ange namn på alla spelare: ")
spelare_namn = spelare_namn.split(', ')

antal_spelare = len(spelare_namn)
aktiva_spelare = alla_spelare[:antal_spelare]
aktiva_poäng = alla_poäng[:antal_spelare]

gi_min = [1, 7, 13, 19, 25, 31, 37, 43, 49, 55]
gi_max = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]


# -------------------
# FUNKTIONER
# -------------------


def blanda_kort(hög):
    random.shuffle(hög)
    return hög


def blanda_kort_igen():
    sakhög.clear()
    for i in range(1, 61):
        kortlek.append(i)
    blanda_kort(kortlek)
    sakhög.append(kortlek[0])


def visa_kort(hand):
    for kort in hand:
        print(10 - hand.index(kort), ":", kort)


def kortutdelning(alla_spelare, lek, sakhög):
    blanda_kort(lek)
    for spelare in alla_spelare:
        for _ in range(10):
            kort = lek.pop(0)
            spelare.append(kort)
    sakhög.append(lek.pop(0))
    return alla_spelare


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
        poäng += poäng_bricka(aktiva_spelare[tur])
        aktiva_poäng[tur] = poäng
        return aktiva_poäng[tur]


def spelrunda(spelare, kortlek, sakhög):
    # visa_kort(spelare)
    print(spelare)
    print("Sakhög:", sakhög[-1])

    val = (input("Ta upp? ja/nej: "))
    if val == "ja" or val == "Ja":
        byta = int(input("Byta (index): "))
        spelare.insert(byta - 1, sakhög.pop(-1))
        sakhög.append(spelare.pop(byta))
        print(spelare)
        print("\n\n")


    elif val == "nej" or val == "Nej":
        print("\n")
        print("Kortlek:", kortlek[0], " ", "Sakhög:", sakhög[-1])
        val = (input("Behålla ja/nej: "))

        if val == "ja" or val == "Ja":
            byta = int(input("Byta (index): "))
            spelare.insert(byta - 1, kortlek.pop(0))
            sakhög.append(spelare.pop(byta))
            print(spelare, "\n", "\n")
            print("")

        elif val == "nej" or val == "Nej":
            sakhög.append(kortlek.pop(0))
            print("")

    elif val == "vinn":
        spelare.sort()
        print("")


def intervall_check(spelare):
    godkända_kort = []
    for k in range(0, 10):
        if gi_min[k] <= spelare[k] <= gi_max[k]:
            godkända_kort.append(spelare[k])
        else:
            godkända_kort.append(False)
    return godkända_kort


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


def jarvis(godkända_kort, spelare):
    while True:
        # kollar för sakhögen
        if godkända_kort[0] == False and godkända_kort[1] == True and (sakhög[-1] <= spelare[1]):
            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, sakhög[-2])
            print(sakhög[-2], 1, "sakhög 1")
            return spelare

        elif godkända_kort[0] == False and (sakhög[-1] <= Adjust_Interval(intervall_check(spelare))[0]):
            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, sakhög[-2])
            print(sakhög[-2], 1, "sakhög 1.5")
            return spelare

        elif godkända_kort[9] == False and godkända_kort[8] == True and (spelare[8] < sakhög[-1]):
            sakhög.append(spelare[9]), spelare.pop(9)
            spelare.insert(9, sakhög[-2])
            print(sakhög[-2], 10, "sakhög 2")
            return spelare

        for j in range(1, 10):
            if godkända_kort[j] == False and (Adjust_Interval(intervall_check(spelare))[j - 1] < sakhög[-1] <=
                                              Adjust_Interval(intervall_check(spelare))[j]):
                sakhög.append(spelare[j]), spelare.pop(j)
                spelare.insert(j, sakhög[-2])
                print(sakhög[-2], j + 1, "sakhög 3")
                return spelare

        # kollar kortleken
        if godkända_kort[0] == False and godkända_kort[1] == True and (kortlek[0] <= spelare[1]):

            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, kortlek[0]), kortlek.pop(0)
            print(spelare[0], 1, "kortlek 1")
            return spelare

        elif godkända_kort[9] == False and godkända_kort[8] == True and (
                kortlek[0] <= Adjust_Interval(intervall_check(spelare))[0]):
            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, kortlek[0])
            print(spelare[0], 1, "kortlek 1.5")
            return spelare

        elif godkända_kort[9] == False and godkända_kort[8] == True and (spelare[8] <= kortlek[0]):
            sakhög.append(spelare[9]), spelare.pop(9)
            spelare.insert(9, kortlek[0]), kortlek.pop(0)
            print(spelare[9], 10, "kortlek 2")
            return spelare

        for k in range(1, 10):
            if godkända_kort[k] == False and (Adjust_Interval(intervall_check(spelare))[j - 1] < kortlek[0] <=
                                              Adjust_Interval(intervall_check(spelare))[j]):
                sakhög.append(spelare[k]), spelare.pop(k)
                spelare.insert(k, kortlek[0]), kortlek.pop(0)
                print(spelare[k], k + 1, "kortlek 3")
                return spelare

        print("botten bytar ingen")
        sakhög.append(kortlek[0]), kortlek.pop(0)
        return spelare


def gi(godkända_kort, spelare):
    for j in range(len(godkända_kort)):
        if godkända_kort[j] == False and gi_min[j] <= sakhög[-1] <= gi_max[j]:
            sakhög.append(spelare[j]), spelare.pop(j)
            spelare.insert(j, sakhög[-2])
            print(sakhög[-2], j + 1, "sakhög")
            return spelare

    for k in range(len(godkända_kort)):
        if godkända_kort[k] == False and gi_min[k] <= kortlek[0] <= gi_max[k]:
            sakhög.append(spelare[k]), spelare.pop(k)
            spelare.insert(k, kortlek[0]), kortlek.pop(0)
            print(spelare[k], k + 1, "kortlek")
            return spelare

    print("botten byter ingen")
    sakhög.append(kortlek[0]), kortlek.pop(0)
    return spelare


def Petter(godkända_kort, spelare):
    j = 0
    if godkända_kort[j] == False and gi_min[j] <= sakhög[-1] <= gi_max[j]:
        sakhög.append(spelare[j]), spelare.pop(j)
        spelare.insert(j, sakhög[-2])
        print(sakhög[-2], j + 1, "sakhög", j + 1)
        j += 1
        return spelare

    elif godkända_kort[j] == False and gi_min[j] <= kortlek[0] <= gi_max[j]:
        sakhög.append(spelare[j]), spelare.pop(j)
        spelare.insert(j, kortlek[0]), kortlek.pop(0)
        print(spelare[j], j + 1, "kortlek", j + 1)
        j += 1
        return spelare

    print("botten byter ingen")
    sakhög.append(kortlek[0]), kortlek.pop(0)
    return spelare


def risk(godkända_kort, spelare):
    while True:
        # kollar för sakhögen
        if godkända_kort[0] == False and godkända_kort[1] == True and (sakhög[-1] <= spelare[1]):
            print(sakhög[-1], 1, "sakhög 1")
            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, sakhög[-2])
            return False

        elif godkända_kort[0] == False and (sakhög[-1] <= Adjust_Interval(intervall_check(spelare))[0]):
            print(sakhög[-1], 1, "sakhög 1.5")
            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, sakhög[-2])
            return False

        elif godkända_kort[9] == False and godkända_kort[8] == True and (spelare[8] < sakhög[-1]):
            print(sakhög[-1], 10, "sakhög 2")
            sakhög.append(spelare[9]), spelare.pop(9)
            spelare.insert(9, sakhög[-2])
            return False

        for k in range(0, 9):
            if godkända_kort[k] != False and (godkända_kort[k] + 1) == sakhög[
                -1]:  # om sakhögen är en mer än det som finns på godkännt index
                sakhög.append(spelare[k + 1]), spelare.pop(k + 1)
                spelare.insert((k + 1), sakhög[-2])
            else:
                continue

        for m in range(1, 10):
            if godkända_kort[k] != False and (godkända_kort[m] - 1) == sakhög[
                -1]:  # om sakhögen är en mindre än det som finns på godkännt index
                sakhög.append(spelare[m - 1]), spelare.pop(m - 1)
                spelare.insert((m - 1), sakhög[-2])
            else:
                continue

        for j in range(1, 10):
            if godkända_kort[j] == False and (Adjust_Interval(intervall_check(spelare))[j - 1] < sakhög[-1] <=
                                              Adjust_Interval(intervall_check(spelare))[j]):
                print(sakhög[-1], j + 1, "sakhög 3")
                sakhög.append(spelare[j]), spelare.pop(j)
                spelare.insert(j, sakhög[-2])
                return False

        # kollar kortleken
        if godkända_kort[0] == False and godkända_kort[1] == True and (kortlek[0] <= spelare[1]):
            print(kortlek[0], 1, "kortlek 1")
            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, kortlek[0]), kortlek.pop(0)
            return False

        elif godkända_kort[9] == False and godkända_kort[8] == True and (
                kortlek[0] <= Adjust_Interval(intervall_check(spelare))[0]):
            print(sakhög[-1], 1, "kortlek 1.5")
            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, kortlek[0])
            return False

        elif godkända_kort[9] == False and godkända_kort[8] == True and (spelare[8] <= kortlek[0]):
            print(kortlek[0], 10, "kortlek 2")
            sakhög.append(spelare[9]), spelare.pop(9)
            spelare.insert(9, kortlek[0]), kortlek.pop(0)
            return False

        for k in range(0, 9):
            if godkända_kort[k] != False and (godkända_kort[k] + 1) == kortlek[
                0]:  # om korthögen är en mer än det som finns på godkännt index
                sakhög.append(spelare[k + 1]), spelare.pop(k + 1)
                spelare.insert((k + 1), sakhög[-2])
            else:
                continue

        for k in range(1, 10):
            if godkända_kort[k] != False and (godkända_kort[k] - 1) == kortlek[
                0]:  # om kortleken är en mindre än det som finns på godkännt index
                sakhög.append(spelare[k - 1]), spelare.pop(k - 1)
                spelare.insert((k - 1), sakhög[-2])

        for k in range(1, 10):
            if godkända_kort[k] == False and (Adjust_Interval(intervall_check(spelare))[j - 1] < kortlek[0] <=
                                              Adjust_Interval(intervall_check(spelare))[j]):
                print(kortlek[0], k + 1, "kortlek 3")
                sakhög.append(spelare[k]), spelare.pop(k)
                spelare.insert(k, kortlek[0]), kortlek.pop(0)
                return False

        print("botten byter inget", sakhög[-1], kortlek[0])
        sakhög.append(kortlek[0]), kortlek.pop(0)
        return False


def högen(godkända_kort, spelare):
    for j in range(len(godkända_kort)):
        if godkända_kort[0] == False and godkända_kort[1] == True and (sakhög[-1] <= spelare[1]):
            godkända_kort.pop(0), godkända_kort.insert(0, sakhög[-1])
            sakhög.append(spelare[0]), spelare.pop(0)
            spelare.insert(0, sakhög[-2])
            print(sakhög[-2], 1, "sakhög 1")
            return spelare

        elif godkända_kort[9] == False and godkända_kort[8] == True and (spelare[8] < sakhög[-1]):
            sakhög.append(spelare[9]), spelare.pop(9)
            spelare.insert(9, sakhög[-2])
            print(sakhög[-2], 10, "sakhög 2")
            return spelare

        elif godkända_kort[j] == False and gi_min[j] <= sakhög[-1] <= gi_max[j]:
            godkända_kort.pop(9), godkända_kort.insert(9, sakhög[-1])
            sakhög.append(spelare[j]), spelare.pop(j)
            spelare.insert(j, sakhög[-2])
            print(sakhög[-2], j + 1, "sakhög 3")
            return spelare

    print("botten bytar ingen")
    sakhög.append(kortlek[0]), kortlek.pop(0)
    return spelare


def simulering(omgångar):
    for ___ in range(omgångar):
        pass

    aktiva_spelare = kortutdelning(aktiva_spelare, kortlek, sakhög)

    for tur in range(0, antal_spelare):

        if len(kortlek) <= 1:
            for i in range(1, 61):
                kortlek.append(i)
            sakhög.clear()
            blanda_kort(kortlek)
            sakhög.append(kortlek[0])
            # print("kortleken blandas")

        if spelare_namn[tur] == "jarvis":
            print(aktiva_spelare[tur], sakhög[-1], kortlek[0])
            print(jarvis(intervall_check(aktiva_spelare[tur]), aktiva_spelare[tur]), sakhög[-1], kortlek[0])

        elif spelare_namn[tur] == "gi":
            print(aktiva_spelare[tur], sakhög[-1], kortlek[0])
            print(gi(intervall_check(aktiva_spelare[tur]), aktiva_spelare[tur]), sakhög[-1], kortlek[0])

        elif spelare_namn[tur] == "petter":
            print(aktiva_spelare[tur], sakhög[-1], kortlek[0])
            print(Petter(intervall_check(aktiva_spelare[tur]), aktiva_spelare[tur]), sakhög[-1], kortlek[0])

        elif spelare_namn[tur] == "högen":
            print(aktiva_spelare[tur], sakhög[-1], kortlek[0])
            print(högen(intervall_check(aktiva_spelare[tur]), aktiva_spelare[tur]), sakhög[-1], kortlek[0])

        if aktiva_spelare[tur] == sorted(aktiva_spelare[tur]):
            print("\nRundan har avslutats då", spelare_namn[tur],
                  "har fått Rack-o!\n\nHär är den nuvarande poängställningen:")
            Räkna_Poäng(aktiva_poäng, aktiva_spelare[tur], aktiva_spelare)


# -------------------
# SJÄLVA SPELET
# -------------------

rounds = 0
omgång = 0


def racko_check(spelare):
    for hand in spelare:
        if hand == sorted(hand):
            return False
        else:
            return True

def poäng_check(spelare):
    for poäng in spelare:
        if poäng >= 500:
            return False
        else:
            return True

def work_in_progess(spelare,lek,hög):
    kortlek.clear()
    for k in range(len(spelare)):
        spelare[k].clear()

    for i in range(1, 61):
        lek.append(i)

    hög.clear()
    blanda_kort(lek)


aktiva_spelare = kortutdelning(aktiva_spelare, kortlek, sakhög)

while poäng_check(aktiva_poäng):
    if not racko_check(aktiva_spelare):
        work_in_progess(aktiva_spelare, kortlek, sakhög)
        aktiva_spelare = kortutdelning(aktiva_spelare, kortlek, sakhög)
        #blanda_kort(aktiva_spelare)
        omgång += 1
        print("\n--------------------------------------------------------\n")
        print("ny runda (",omgång,")")

        for tur in range(len(aktiva_spelare)):
            print(spelare_namn[tur], Räkna_Poäng(aktiva_poäng, aktiva_spelare[tur], aktiva_spelare))

    while racko_check(aktiva_spelare):
        for tur in range(0, antal_spelare):
            rounds += 1
            if len(kortlek) <= 1:
                sakhög.clear()
                for i in range(1, 61):
                    kortlek.append(i)

                blanda_kort(kortlek)
                sakhög.append(kortlek[0])
                print("kortleken blandas")

            print("\n--------------------------------------------------------\n")
            print(spelare_namn[tur], " ", tur + 1, "'s tur", sep='')

            if spelare_namn[tur] == "jarvis":
                print(aktiva_spelare[tur], sakhög[-1], kortlek[0])
                print(jarvis(intervall_check(aktiva_spelare[tur]), aktiva_spelare[tur]), sakhög[-1], kortlek[0])

            elif spelare_namn[tur] == "gi":
                print(aktiva_spelare[tur], sakhög[-1], kortlek[0])
                print(gi(intervall_check(aktiva_spelare[tur]), aktiva_spelare[tur]), sakhög[-1], kortlek[0])

            elif spelare_namn[tur] == "petter":
                print(aktiva_spelare[tur], sakhög[-1], kortlek[0])
                print(Petter(intervall_check(aktiva_spelare[tur]), aktiva_spelare[tur]), sakhög[-1], kortlek[0])

            elif spelare_namn[tur] == "högen":
                print(aktiva_spelare[tur], sakhög[-1], kortlek[0])
                print(högen(intervall_check(aktiva_spelare[tur]), aktiva_spelare[tur]), sakhög[-1], kortlek[0])

            if aktiva_spelare[tur] == sorted(aktiva_spelare[tur]):
                Räkna_Poäng(aktiva_poäng, aktiva_spelare[tur], aktiva_spelare)
                print("\n", spelare_namn[tur], tur + 1, "fick rack-o")
                print(racko_check(aktiva_spelare))
                break


for tur in range(len(aktiva_spelare)):
    print(spelare_namn[tur], Räkna_Poäng(aktiva_poäng, aktiva_spelare[tur], aktiva_spelare))