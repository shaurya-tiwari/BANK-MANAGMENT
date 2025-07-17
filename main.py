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
    database = 'data.json'  # file name
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
    def __update(cls):  # from these underscore now only class can call the update method
        # Bank also written as bank becouse that also target the class bank
        with open(cls.database, 'w') as fs:
            # wrieta ll the daata in data,json file ..
            fs.write(json.dumps(cls.data))

    @classmethod
    def __accountgenerte(cls):  # private class method
        # we want 3 string , K IS thheh vaue of random generation
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)  # 3 numbers as wel
        # oly one special character
        spchar = random.choices('!@#$%^&*()_', k=1)
        id = alpha+num+spchar
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
            "balance": 0
        }
        if info["age"] < 18 or len(str(info['PIN'])) != 4:
            print("sorry you are not allowed to creret your accouNT.")
        else:
            print("______________________________________ACCOUNT CREATED SUCCESFULY")
            for i in info:
                print(f"{i}: {info[i]}")  # {}for key , [] for values
            print(f" ! NOTE YOUR CCCOUNT NUMBER ! {info['AccountNumber']}")
            # after thsi all senerio , now update data ot teh json file which is called as data frpm the info
            Bank.data.append(info)
            Bank.__update()

    def depositemonney(self):
        accountnumber = input("Enter account number : ")
        pin = int(input("Enter 4 digit PIN :"))

        userdata = [i for i in Bank.data if i['AccountNumber'] == accountnumber and i['PIN'] == pin]

        if userdata == False:  # if user data is empty
            print("no data found ! ")
        else:
            amount = int(input("enter amount for deposite : "))
            if amount > 10000 and amount < 0:
                print("entter amount less then 10000! ")
            else:
                print(userdata)
                userdata[0]['balance'] += amount  # update amount in data json
                Bank.__update()
                print("Amount deposited succesfully . ")
                

user = Bank()  # object for bank

print("pres 1 for create account ")
print("pres 2 for depositing the money in the bank ")
print("pres 3 for withdrawing the money  ")
print("pres 4 for details   ")
print("pres 5  f or updatte detials ")
print("pres 6 ")

check = int(input("tell ut response : "))

if check == 1:
    user.createaccount()

if check == 2:
    user.depositemonney()
