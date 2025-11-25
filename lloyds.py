

from itertools import combinations

färg_dict = {"spader": 0, "klöver": 0, "ruter": 0, "hjärter": 0}
valör_dict = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
färg_list = []
valör_list = []
int_valör_list = []


def player_input():
    färg, valör = input(f"kort {len(valör_list) + 1}: ").split(" ")  # ValueError om inte split, KeyError om key inte med i dic

    if valör == "knäckt":
        valör = 11

    elif valör == "dam":
        valör = 12

    elif valör == "kung":
        valör = 13

    elif valör == "ess":
        valör = 14

    färg_list.append(färg)
    valör_list.append(int(valör))
    färg_dict[färg] += 1
    valör_dict[int(valör)] += 1



def par_triss_fyrtal_färg(antal, dic):
    for i in dic.values():
        if i == antal:
            return True

def tvåpar(dic):
    antal_par = 0

    for i in dic.values():
        if i == 2:
            antal_par += 1

    if antal_par == 2:
        return True

def stege(lista):
    count = 1

    if 14 in lista:
        lista.append(1)

    for i in range(1,len(lista)):
        if lista[i] == lista[i-1] + 1:
           count += 1
        else:
            count = 1

    if count == 5:
        return True

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





def pre_flop_eval():
    if par_triss_fyrtal_färg(2,valör_dict):
        return "par"

    return f"high card ({high_card(valör_list):})"

def hand_eval():
    # ANTECKNING
    # färgstege (färg + stege)

    # fyrtal
    if par_triss_fyrtal_färg(4, valör_dict):
        return "fyrtal"


    # kåk (triss + par)
    elif par_triss_fyrtal_färg(2, valör_dict) and par_triss_fyrtal_färg(3, valör_dict):
        return "kåk"


    # färg (5 av samma färg)
    elif par_triss_fyrtal_färg(5, färg_dict):
        return "färg"


    # stege - (5 kort med valörer i direkt följd)
    elif stege(sorted(valör_list)):
        return "stege"

    # triss
    elif par_triss_fyrtal_färg(3, valör_dict):
        return "triss"

    # tvåpar
    elif tvåpar(valör_dict):
        return "tvåpar"

    # par
    elif par_triss_fyrtal_färg(2, valör_dict):
        return "par"

    # högt kort
    else:
        return f"high card ({high_card(valör_list):})"






print("Pre-flop")
for i in range(2):
    player_input()

print(list(combinations(valör_list,2)))
print(pre_flop_eval())
print("\n------------------------------------------\n")

print("Flop")
for i in range(3):
    player_input()

print(list(combinations(valör_list,5)))
print(hand_eval())
print("\n------------------------------------------\n")

print("Turn")
player_input()

print(list(combinations(valör_list,5)))
print(hand_eval())
print("\n------------------------------------------\n")

print("River")
player_input()

print(list(combinations(valör_list,5)))
print(hand_eval())
print("\n------------------------------------------\n")

print(färg_list)
print(valör_list)
print(list(combinations(valör_list,5)))

