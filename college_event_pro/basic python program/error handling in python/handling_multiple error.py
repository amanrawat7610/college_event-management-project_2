try:
    x=int(input("enter the value: \n"))
    y=15/x
    print("the value of y is:",y)

except ValueError:
    print("enter a correct value!")
except ZeroDivisionError:
    print("division by zero is not allowed!")        
