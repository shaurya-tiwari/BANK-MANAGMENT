import json
import random
import string
from pathlib import Path
import streamlit as st


class Bank:
    database = "data.json"
    data = []

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database) as fs:
                cls.data = json.load(fs)
        else:
            cls.data = []
            with open(cls.database, "w") as fs:
                json.dump(cls.data, fs)

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __account_generate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*()_", k=1)
        acc_id = alpha + num + spchar
        random.shuffle(acc_id)
        return "".join(acc_id)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return "Sorry, you must be at least 18 and enter a 4-digit PIN."

        account_number = cls.__account_generate()
        info = {
            "name": name,
            "age": age,
            "email": email,
            "PIN": pin,
            "AccountNumber": account_number,
            "balance": 0,
        }
        cls.data.append(info)
        cls.__update()
        return f"Account created successfully! Your Account Number is: {account_number}"

    @classmethod
    def deposit_money(cls, account_number, pin, amount):
        user = cls.__find_user(account_number, pin)
        if not user:
            return "No user found."
        if amount <= 0 or amount > 10000:
            return "Amount should be between 1 and 10,000."

        user["balance"] += amount
        cls.__update()
        return f"Deposited ₹{amount}. New balance: ₹{user['balance']}"

    @classmethod
    def withdraw_money(cls, account_number, pin, amount):
        user = cls.__find_user(account_number, pin)
        if not user:
            return "No user found."
        if amount <= 0:
            return "Amount should be greater than 0."
        if user["balance"] < amount:
            return "Insufficient balance."

        user["balance"] -= amount
        cls.__update()
        return f"Withdrew ₹{amount}. New balance: ₹{user['balance']}"

    @classmethod
    def show_details(cls, account_number, pin):
        user = cls.__find_user(account_number, pin)
        return user if user else "No user found."

    @classmethod
    def update_details(cls, account_number, pin, name=None, email=None, new_pin=None):
        user = cls.__find_user(account_number, pin)
        if not user:
            return "No user found."

        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if new_pin:
            if len(str(new_pin)) == 4:
                user["PIN"] = new_pin
            else:
                return "New PIN must be 4 digits."

        cls.__update()
        return "Details updated successfully."

    @classmethod
    def delete_account(cls, account_number, pin):
        user = cls.__find_user(account_number, pin)
        if not user:
            return "No user found."

        cls.data.remove(user)
        cls.__update()
        return "Account deleted successfully."

    @classmethod
    def __find_user(cls, account_number, pin):
        for i in cls.data:
            if i["AccountNumber"] == account_number and i["PIN"] == pin:
                return i
        return None


# Streamlit UI
st.title("🏦 Simple Bank App")

Bank.load_data()

menu = st.sidebar.selectbox(
    "Menu",
    ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Details", "Delete Account"]
)

if menu == "Create Account":
    st.header("Create New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", max_chars=4)
    if st.button("Create"):
        if name and age and email and pin:
            res = Bank.create_account(name, age, email, int(pin))
            st.success(res)
        else:
            st.warning("Please fill all fields.")

elif menu == "Deposit Money":
    st.header("Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=0, step=1)
    if st.button("Deposit"):
        if acc and pin and amount:
            res = Bank.deposit_money(acc, int(pin), amount)
            st.success(res)
        else:
            st.warning("Please fill all fields.")

elif menu == "Withdraw Money":
    st.header("Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=0, step=1)
    if st.button("Withdraw"):
        if acc and pin and amount:
            res = Bank.withdraw_money(acc, int(pin), amount)
            st.success(res)
        else:
            st.warning("Please fill all fields.")

elif menu == "Show Details":
    st.header("Show Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    if st.button("Show"):
        if acc and pin:
            res = Bank.show_details(acc, int(pin))
            if isinstance(res, dict):
                st.json(res)
            else:
                st.error(res)
        else:
            st.warning("Please fill all fields.")

elif menu == "Update Details":
    st.header("Update Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    name = st.text_input("New Name")
    email = st.text_input("New Email")
    new_pin = st.text_input("New PIN (4 digits)")
    if st.button("Update"):
        if acc and pin:
            res = Bank.update_details(
                acc,
                int(pin),
                name=name if name else None,
                email=email if email else None,
                new_pin=int(new_pin) if new_pin else None,
            )
            st.success(res)
        else:
            st.warning("Please provide account number and PIN.")

elif menu == "Delete Account":
    st.header("Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    if st.button("Delete"):
        if acc and pin:
            res = Bank.delete_account(acc, int(pin))
            st.success(res)
        else:
            st.warning("Please fill all fields.")
