student={
    "name":"aman",
    "city":"delhi",
    "company":"tata"
}
student.pop("name")
print(student)

print(student.keys)

student["class"]= "12th"
print(student)

student.popitem()
print(student)

del student["city"]
print(student)

print(student.values())
print(student.items())