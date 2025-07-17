# for save user data for not regenerate afyer reenter in then code we sue json file (java script object notation)
import json
import random
import string
from pathlib import Path


# bank features
# bank account
# withdraw mone
# bank details
# update derails
# delete account


# main helper clas


class Bank:
    database = "data.json"  # file name
    data = []  # al te adta / dummy  data
    try:
        if Path(database).exists():  # if file exist the open other wise not
            with open(database) as fs:  # load every data in data variable
                data = json.load(fs)
        else:
            print("no such file exists ")
    except Exception as err:
        print(f"an excetion occured{err}")

    @classmethod  # for not accsing any one
    def __update(
        cls,
    ):  # from these underscore now only class can call the update method
        # Bank also written as bank becouse that also target the class bank
        with open(cls.database, "w") as fs:
            # wrieta ll the daata in data,json file ..
            fs.write(json.dumps(cls.data))

    @classmethod
    def __accountgenerte(cls):  # private class method
        # we want 3 string , K IS thheh vaue of random generation
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)  # 3 numbers as wel
        # oly one special character
        spchar = random.choices("!@#$%^&*()_", k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        # this is beecouse when i shuffle the chars then we get list for that we oin all the char for  ssingle line string
        return "".join(id)

    def createaccount(self):
        info = {  # store data in the foem of  key ans value pair
            "name": input("name :-"),
            "age": int(input("age:-")),
            "email": input("email id : "),
            "PIN": int(input(" 4 digit PIN:- ")),
            "AccountNumber": Bank.__accountgenerte(),
            "balance": 0,
        }
        if info["age"] < 18 or len(str(info["PIN"])) != 4:
            print("sorry you are not allowed to creret your accouNT.")
        else:
            print(
                "______________________________________________________! ACCOUNT CREATED SUCCESFULY !____________________________________________________"
            )
            for i in info:
                print(f"{i}: {info[i]}")  # {}for key , [] for values
            print(f" ! NOTE YOUR CCCOUNT NUMBER ! {info['AccountNumber']}")
            # after thsi all senerio , now update data ot teh json file which is called as data frpm the info
            Bank.data.append(info)
            Bank.__update()

    def depositemonney(self):
        accountnumber = input("Enter account number : ")
        pin = int(input("Enter 4 digit PIN :"))

        userdata = [
            i
            for i in Bank.data
            if i["AccountNumber"] == accountnumber and i["PIN"] == pin
        ]

        if userdata == False:  # if user data is empty
            print("no data found ! ")
        else:
            amount = int(input("enter amount for deposite : "))
            if amount > 10000 and amount < 0:
                print("entter amount less then 10000! ")
            else:
                # NOTE: use 0 index for the data , come in the list at the index first whicih is zero
                userdata[0]["balance"] += amount  # update amount in data json
                Bank.__update()
                print("Amount deposited succesfully . ")
                print(userdata)

    def withdrawmoney(self):
        accountnumber = input("Enter account number : ")
        pin = int(input("Enter 4 digit PIN :"))

        userdata = [
            i
            for i in Bank.data
            if i["AccountNumber"] == accountnumber and i["PIN"] == pin
        ]
        if userdata == False:  # if user data is empty
            print("no data found ! ")
        else:
            amount = int(input("enter withdrawel amoun: "))
            if userdata[0]["balance"] < amount:
                print("insufficient amoount !")
            else:
                # NOTE: use 0 index for the data , come in the list at the index first whicih is zero
                userdata[0]["balance"] -= amount  # update amount in data json
                Bank.__update()
                print("Amount withdrawn succesfully . ")
                print(userdata)

    # NOTE:  we use self becouse its  call by object
    def showdetails(self):
        accountnumber = input("Enter account number : ")
        pin = int(input("Enter 4 digit PIN :"))
        userdata = [
            i
            for i in Bank.data
            if i["AccountNumber"] == accountnumber and i["PIN"] == pin
        ]
        print("personal details \n")
        for i in userdata[0]:
            print(f"{i}: {userdata[0][i]}")

    def updatedetails(self):
        accountnumber = input("Enter account number : ")
        pin = int(input("Enter 4 digit PIN :"))
        userdata = [
            i
            for i in Bank.data
            if i["AccountNumber"] == accountnumber and i["PIN"] == pin
        ]
        if userdata == False:
            print("user not found !")
        else:
            print("you can't change (age, accNO and balance)\n")
            print("fill deatails for change or leave it empty\n")

            newdata = {
                "name": input("enter new name or press enter for skip."),
                "email": input("enter new email or press entter to skip."),
                "PIN": input("enter new pin or pree enter to skip."),
            }

            if newdata["name"] == "":
                newdata["name"] == userdata[0]["name"]
            if newdata["email"] == "":
                newdata["email"] == userdata[0]["email"]
            if newdata["PIN"] == "":
                newdata["PIN"] == userdata[0]["PIN"]

            newdata["age"] = userdata[0]["age"]
            newdata["AccountNumber"] = userdata[0]["AccountNumber"]
            newdata["balance"] = userdata[0]["balance"]

            if type(newdata["PIN"]) == str:
                newdata["PIN"] = int(newdata["PIN"])

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]

            Bank.__update()
            print("deatails updated succesfully.")

    def deletfuntion(self):
        accountnumber = input("Enter account number : ")
        pin = int(input("Enter 4 digit PIN :"))
        userdata = [
            i
            for i in Bank.data
            if i["AccountNumber"] == accountnumber and i["PIN"] == pin
        ]
        if userdata == False:
            print("user  not found !")
        else:
            check = input("coution ! DELETE ACCOUNT ? y/n : ").lower()
            if check == "n":
                print("operation canceled")
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("account deleted succesfully !")
            Bank.__update()


user = Bank()  # object for bank

print("pres 1 for create account ")
print("pres 2 for depositing the money in the bank ")
print("pres 3 for withdrawing the money  ")
print("pres 4 for personnal details   ")
print("pres 5  for updatte detials ")
print("pres 6 ")

check = int(input("tell ut response : "))

if check == 1:
    user.createaccount()

if check == 2:
    user.depositemonney()

if check == 3:
    user.withdrawmoney()

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()

if check == 6:
    user.deletfuntion()
