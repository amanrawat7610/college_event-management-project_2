x=12 #global varriable
def number():
    global x #Keywords for change global varriable value
    x=22
    print(x)
number()
print(x)