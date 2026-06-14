student={
"name":"aman",
"city":"delhi",
"company":"tata steel"}
print(student)

print(student["company"])
print(student["city"])
# print(student["namee"])  # error
print(student.get("namme"))

student["city"]="rishikesh"
print(student)