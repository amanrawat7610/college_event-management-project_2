import pyperclip
import os

File_Name="password.txt"


def save_password():
    website=input("enter the website ")
    password=input("enter the password")
    with open(File_Name,"a") as f:
        f.write(f"{website}<||>{password}\n")
   
def get_password():
    website=input("enter the website ")
    with open(File_Name,"r") as f:
        for line in f:
            data=line.strip().split("<||>")
            if website in line:
                password=line.strip().split("<||>")[1]
                pyperclip.copy(password)
                print("password copied to clipboard")
                break
        else:
            print("website not found in the password manager")

def main():
    while True:
        print("1.   save password")
        print("2.   get  password")
        print("3.   exit")
        choice=input("choose an option")

        if choice=="1":
            save_password()
        elif choice=="2":
            get_password()
        elif choice=="3":
            print("exiting..")
            break
        else:
            print("Invalid choice!  try next time...")
main()
