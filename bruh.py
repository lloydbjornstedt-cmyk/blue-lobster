""""
inlämning 1 uppgift 2
skapad 13/9
senaste uppdatering
14/9 - ändra primtal_faktorer
27/9 - failsafe med specialfallen då användaren anger n<0 och n=1
29/9 - la till primtal_check samt dess användningar

skapa ett program som utvärderar primtal


steg 1
p är listan som sparar alla faktorer
primtalsfunktionen append:ar alla i som jämt delar n till p
for loop för att iterera alla möjliga faktorer
while loopen dividerar bort alla faktorer

steg 2
användaren får välja n
tar hänsyn till special fallen
kollar om p har några element för att avgöra om n har faktorer

steg 3
2 är redan i q då for-loopen bara itererar udda tal
lägger till j i listan q om primtal_check är True (dvs om j är ett primtal)



"""
#steg 1

def primtal_check(x):
    for i in range(2,int(x**0.5)+1):
        if x%i == 0:
            return False

    return True

p = []
def primtal_faktorer(x):
    for i in range(2,x):
        while x%i == 0:
            print(x)
            p.append(i)
            x = x//i
        if x == 1:
            break


#steg 2
n = int(input("n = "))

if n < 0:
    print("negativa tal kan inte vara inte primtal")

elif n==1:
    print("1 är inte ett primtal")

else:
    if primtal_check(n):
        print(n, "är ett primtal")
    else:
        primtal_faktorer(n)
        print(p)
        print(n,"är inte ett primtal")


# steg 3
q = [2]
for j in range(3, 101, 2):
    if primtal_check(j):
        q.append(j)
print(q)
