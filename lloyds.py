

#idé omvandla ett kort till hexadecimal 


#kan inte koppla valör och färg
#färg_dict = {"spader":0, "klöver":0, "ruter":0, "hjärter":0}
valör_dict = {"2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "knäckt":0, "drottning":0, "kung":0, "ess":0}

färg_lista = []
valör_lista = []

count = 1

class Card:
    def __init__(self):
        self.färg, self.valör = input(f"{len(valör_lista)+1}: ").split(" ")  #ValueError om inte split, KeyError om input inte är med i en dict

        #self.kort = self.färg, self.valör
        #färg_dict[self.färg] += 1
        valör_dict[self.valör] += 1
        färg_lista.append(self.färg)
        valör_lista.append(self.valör)


def utv_hand():
    for i in valör_dict.values():
        if i == 4:
            return "fyrtal"

        elif i == 3:
            return "triss"

        elif i == 2:
            return "par"

    return "just fold bro"


print("\n")
print("Handen")
for i in range(2):
    hand = Card()

print("\n", utv_hand())
print("\n------------------------------------------\n")


print("Flop")
for i in range(3):
    flop = Card()

print("\n", utv_hand())
print("\n------------------------------------------\n")


print("Turn")
turn = Card()

print("\n", utv_hand())
print("\n------------------------------------------\n")


print("River")
river = Card()

print("\n", utv_hand())
print("\n------------------------------------------\n")


print(färg_lista)
print(valör_lista)






"""
print(färg_dict)
print(valör_dict)

for i in valör_dict.values(): #values är antalet av varje key
    if i == 2: #om det finns två av samma kort (par)
        print("call")
        break
    else:
        print("fold")
        break
"""

# ANTECKNING
# färgstege - N/A (färg + stege)
# fyrtal - *
# kåk - N/A (triss + par)
# färg - N/A (5 av samma färg)
# stege - N/A, behöver ta hänsyn till ess (5 kort med valörer i direkt följd)
# triss - *
# tvåpar - N/A
# par - *
# högt kort - N/A, ge numeriskt värde till klädda kort (bästa kortet)

# alla med * = kollar values i valör_dict med en for-loop