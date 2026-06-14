import random
def game_win(user,computer):
    if user== computer:
        return none

#water and gun
    if user=="w" and computer=="g":
        return True
    if user=="g" and computer=="w":
        return False

#gun and snake
    if user=="g" and computer=="s":
     return True
    if user=="s" and computer=="g":
     return False
#water and snake
    if user=="s" and computer=="w":
     return True
    if user=="w" and computer=="s":
        return False

rand_no=random.randint(1,3)
print("computers turn: snake(s),water(w),gun(g)")   

if rand_no ==1 :
    computer="s"

elif rand_no ==2 :
    computer="w"

else:
    computer="g"

user=print(input("your turn: snake(s),water(w),gun(g)"))
result=game_win(user,computer)
print(f"\n you dcoose:{user}")
print(f"\n computer dcoose:{computer}")

if result is None:
    print("its a draw")
elif(result):
    print("you win")
else:
    print("you lose")