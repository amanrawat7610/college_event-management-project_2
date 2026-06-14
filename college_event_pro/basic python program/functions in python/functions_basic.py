def greet(fname,lname):
    print("what is your name ! ",fname,lname)
    print("how are you")
    print("tankyou")
greet("harry","khan")
greet("aman","rawat")

def add(a,b):
    # print(a+b)
    return a+b
    
c=add(3,4)
print(c)


def greet(name="user",city="delhi"):
    print("hello",name,city)

greet()
greet("rohan")
greet(name="aman",city="mumbaie")