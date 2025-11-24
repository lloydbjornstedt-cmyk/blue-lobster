

färg_dict = {"spader":0, "klöver":0, "ruter":0, "hjärter":0}
valör_dict = {2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0}

färg_list = []
valör_list = []


def player_input():
    färg, valör = input(f"kort {len(valör_list)+1}: ").split(" ")  #ValueError om inte split, KeyError

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


def consecutive():
    pass

def hand_evaluation():
    pass
    # ANTECKNING
    # färgstege (färg + stege)

    # fyrtal
    for i in valör_list:
        if valör_list.count(i) == 4:
            return "fyrtal"


    # kåk (triss + par)


    # färg (5 av samma färg)
    for i in färg_list:
        if färg_list.count(i) == 5:
            return "färg"

    # stege - behöver ta hänsyn till ess (5 kort med valörer i direkt följd)

    # triss
    for i in valör_list:
        if valör_list.count(i) == 3:
            return "triss"

    # tvåpar

    # par
    for i in valör_list:
        if valör_list.count(i) == 2:
            return "par"

    # högt kort
    if 11 <= sorted(valör_list)[-1] <= 14:
        return "high card"

    return "just fold bro"


def player_choice():
    pass



"""
print("\n")
marker = int(input("Antalet marker: "))
print("\n------------------------------------------\n")

while marker >= 0:
"""

print("Pre-flop")
for i in range(2):
    player_input()

print(hand_evaluation())
print("\n------------------------------------------\n")


print("Flop")
for i in range(3):
    player_input()

print(hand_evaluation())
print("\n------------------------------------------\n")


print("Turn")
player_input()

print(hand_evaluation())
print("\n------------------------------------------\n")


print("River")
player_input()

print(hand_evaluation())
print("\n------------------------------------------\n")


print(färg_list)
print(valör_list)
print(färg_dict)
print(valör_dict)





