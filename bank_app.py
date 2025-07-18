import json
import random
import string
from pathlib import Path
import streamlit as st
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="SimpleBank - Digital Banking",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
    }
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #e1e8ed;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .user-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    .balance-amount {
        font-size: 2rem;
        font-weight: bold;
        color: #4CAF50;
    }
    .account-number {
        font-family: monospace;
        font-size: 1.1rem;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem;
        border-radius: 5px;
        display: inline-block;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to show user details in a card
def show_user_card(user):
    st.markdown(f"""
    <div class="user-card">
        <h2>👤 {user['name']}</h2>
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0;">
            <div>
                <p><strong>Account Number:</strong><br>
                <span class="account-number">{user['AccountNumber']}</span></p>
                <p><strong>Email:</strong> {user['email']}</p>
                <p><strong>Age:</strong> {user['age']} years</p>
            </div>
            <div style="text-align: right;">
                <p><strong>Current Balance</strong></p>
                <div class="balance-amount">₹{user['balance']:,}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Helper function for custom messages
def show_message(message, msg_type="info"):
    if msg_type == "success":
        st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
    elif msg_type == "error":
        st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
    elif msg_type == "warning":
        st.markdown(f'<div class="warning-message">⚠️ {message}</div>', unsafe_allow_html=True)

class Bank:
    database = "data.json"
    data = []

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            try:
                with open(cls.database) as fs:
                    cls.data = json.load(fs)
                # Clean up duplicate account numbers
                cls._fix_duplicate_accounts()
            except json.JSONDecodeError:
                cls.data = []
        else:
            cls.data = []
            with open(cls.database, "w") as fs:
                json.dump(cls.data, fs)

    @classmethod
    def _fix_duplicate_accounts(cls):
        """Fix duplicate account numbers by generating new ones"""
        seen_accounts = set()
        updated = False
        
        for user in cls.data:
            if user["AccountNumber"] in seen_accounts:
                # Generate new unique account number
                user["AccountNumber"] = cls.__account_generate()
                updated = True
            seen_accounts.add(user["AccountNumber"])
        
        if updated:
            cls.__update()

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __account_generate(cls):
        """Generate unique account number"""
        prefix = "SB"
        while True:
            account_number = f"{prefix}{random.randint(100000, 999999)}"
            if not any(acc["AccountNumber"] == account_number for acc in cls.data):
                return account_number

    @classmethod
    def create_account(cls, name, age, email, pin):
        # Enhanced validation
        if not name or not name.strip():
            return "Name cannot be empty."
        if age < 18:
            return "You must be at least 18 years old to open an account."
        if not email or "@" not in email or "." not in email:
            return "Please enter a valid email address (e.g., user@example.com)."
        if len(str(pin)) != 4:
            return "PIN must be exactly 4 digits."

        account_number = cls.__account_generate()
        info = {
            "name": name.strip().title(),
            "age": age,
            "email": email.lower().strip(),
            "PIN": str(pin),  # Store as string for consistency
            "AccountNumber": account_number,
            "balance": 0,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        cls.data.append(info)
        cls.__update()
        return f"Account created successfully! Your Account Number is: {account_number}"

    @classmethod
    def deposit_money(cls, account_number, pin, amount):
        user = cls.__find_user(account_number, pin)
        if not user:
            return "Invalid account number or PIN."
        if amount <= 0:
            return "Amount must be greater than 0."
        if amount > 100000:
            return "Maximum deposit limit is ₹1,00,000 per transaction."

        user["balance"] += amount
        cls.__update()
        return f"Successfully deposited ₹{amount:,}. New balance: ₹{user['balance']:,}"

    @classmethod
    def withdraw_money(cls, account_number, pin, amount):
        user = cls.__find_user(account_number, pin)
        if not user:
            return "Invalid account number or PIN."
        if amount <= 0:
            return "Amount must be greater than 0."
        if user["balance"] < amount:
            return f"Insufficient balance. Current balance: ₹{user['balance']:,}"

        user["balance"] -= amount
        cls.__update()
        return f"Successfully withdrew ₹{amount:,}. New balance: ₹{user['balance']:,}"

    @classmethod
    def show_details(cls, account_number, pin):
        user = cls.__find_user(account_number, pin)
        return user if user else "Invalid account number or PIN."

    @classmethod
    def update_details(cls, account_number, pin, name=None, email=None, new_pin=None):
        user = cls.__find_user(account_number, pin)
        if not user:
            return "Invalid account number or PIN."

        updated_fields = []
        if name and name.strip():
            user["name"] = name.strip().title()
            updated_fields.append("name")
        if email and "@" in email and "." in email:
            user["email"] = email.lower().strip()
            updated_fields.append("email")
        if new_pin and len(str(new_pin)) == 4:
            user["PIN"] = str(new_pin)  # Store as string
            updated_fields.append("PIN")
        elif new_pin:
            return "New PIN must be exactly 4 digits."

        if updated_fields:
            cls.__update()
            return f"Successfully updated: {', '.join(updated_fields)}"
        return "No changes were made."

    @classmethod
    def delete_account(cls, account_number, pin):
        user = cls.__find_user(account_number, pin)
        if not user:
            return "Invalid account number or PIN."

        cls.data.remove(user)
        cls.__update()
        return "Account deleted successfully."

    @classmethod
    def __find_user(cls, account_number, pin):
        """Fixed to handle both string and integer PINs"""
        for i in cls.data:
            if i["AccountNumber"] == account_number and str(i["PIN"]) == str(pin):
                return i
        return None

# Initialize bank data
Bank.load_data()

# Header
st.markdown("""
<div class="main-header">
    <h1>🏦 SimpleBank</h1>
    <p style="color: white; font-size: 1.2rem; margin: 0;">Your Digital Banking Partner</p>
</div>
""", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    st.markdown("### 🎯 Banking Services")
    menu = st.selectbox(
        "Choose a service:",
        ["🏠 Dashboard", "➕ Create Account", "💰 Deposit Money", "💸 Withdraw Money", 
         "📊 Show Details", "✏️ Update Details", "🗑️ Delete Account"]
    )
    
    st.markdown("---")
    st.markdown("### 📱 Quick Stats")
    st.info(f"Total Accounts: {len(Bank.data)}")
    
    st.markdown("---")
    st.markdown("### 🔒 Security Note")
    st.warning("Never share your PIN with anyone!")

# Main content area
if menu == "🏠 Dashboard":
    st.markdown("## Welcome to SimpleBank")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🏦 About SimpleBank</h3>
            <p>Your trusted digital banking partner offering secure and convenient banking services.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📈 Quick Stats</h3>
            <p><strong>Total Accounts:</strong> {}</p>
            <p><strong>Active Today:</strong> Online</p>
        </div>
        """.format(len(Bank.data)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>🔧 Services</h3>
            <ul>
                <li>Account Creation</li>
                <li>Money Deposit/Withdrawal</li>
                <li>Account Management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif menu == "➕ Create Account":
    st.markdown("## Open a New Account")
    
    with st.form("create_account_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            age = st.number_input("🎂 Age", min_value=18, max_value=100, value=25)
        
        with col2:
            email = st.text_input("📧 Email Address", placeholder="user@example.com")
            pin = st.text_input("🔐 4-digit PIN", max_chars=4, type="password", placeholder="Enter 4-digit PIN")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            if all([name, age, email, pin]):
                try:
                    result = Bank.create_account(name, age, email, pin)
                    if "successfully" in result:
                        show_message(result, "success")
                        st.balloons()
                    else:
                        show_message(result, "error")
                except ValueError:
                    show_message("PIN must be numeric.", "error")
            else:
                show_message("Please fill all fields.", "warning")

elif menu == "💰 Deposit Money":
    st.markdown("## Deposit Money")
    
    with st.form("deposit_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            acc = st.text_input("🏦 Account Number", placeholder="Enter account number")
            pin = st.text_input("🔐 PIN", type="password", placeholder="Enter your PIN")
        
        with col2:
            amount = st.number_input("💰 Amount (₹)", min_value=1, max_value=100000, value=1000)
        
        submitted = st.form_submit_button("Deposit Money", use_container_width=True)
        
        if submitted:
            if acc and pin:
                try:
                    result = Bank.deposit_money(acc, pin, amount)  # Pass PIN as string
                    if "Successfully" in result:
                        show_message(result, "success")
                        st.balloons()
                    else:
                        show_message(result, "error")
                except ValueError:
                    show_message("Invalid input.", "error")
            else:
                show_message("Please fill all fields.", "warning")

elif menu == "💸 Withdraw Money":
    st.markdown("## Withdraw Money")
    
    with st.form("withdraw_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            acc = st.text_input("🏦 Account Number", placeholder="Enter account number")
            pin = st.text_input("🔐 PIN", type="password", placeholder="Enter your PIN")
        
        with col2:
            amount = st.number_input("💸 Amount (₹)", min_value=1, value=1000)
        
        submitted = st.form_submit_button("Withdraw Money", use_container_width=True)
        
        if submitted:
            if acc and pin:
                try:
                    result = Bank.withdraw_money(acc, pin, amount)  # Pass PIN as string
                    if "Successfully" in result:
                        show_message(result, "success")
                    else:
                        show_message(result, "error")
                except ValueError:
                    show_message("Invalid input.", "error")
            else:
                show_message("Please fill all fields.", "warning")

elif menu == "📊 Show Details":
    st.markdown("## Account Details")
    
    with st.form("show_details_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            acc = st.text_input("🏦 Account Number", placeholder="Enter account number")
        
        with col2:
            pin = st.text_input("🔐 PIN", type="password", placeholder="Enter your PIN")
        
        submitted = st.form_submit_button("Show Account Details", use_container_width=True)
        
        if submitted:
            if acc and pin:
                try:
                    result = Bank.show_details(acc, pin)  # Pass PIN as string
                    if isinstance(result, dict):
                        user = result.copy()
                        user.pop("PIN", None)  # Remove PIN for security
                        show_user_card(user)
                    else:
                        show_message(result, "error")
                except ValueError:
                    show_message("Invalid input.", "error")
            else:
                show_message("Please fill all fields.", "warning")

elif menu == "✏️ Update Details":
    st.markdown("## Update Account Details")
    
    with st.form("update_form"):
        st.markdown("### Current Account Information")
        col1, col2 = st.columns(2)
        
        with col1:
            acc = st.text_input("🏦 Account Number", placeholder="Enter account number")
            pin = st.text_input("🔐 Current PIN", type="password", placeholder="Enter current PIN")
        
        st.markdown("### New Information (Leave blank if no change)")
        col3, col4 = st.columns(2)
        
        with col3:
            name = st.text_input("👤 New Name", placeholder="Enter new name (optional)")
            email = st.text_input("📧 New Email", placeholder="Enter new email (optional)")
        
        with col4:
            new_pin = st.text_input("🔐 New PIN", type="password", placeholder="Enter new PIN (optional)")
        
        submitted = st.form_submit_button("Update Details", use_container_width=True)
        
        if submitted:
            if acc and pin:
                try:
                    result = Bank.update_details(
                        acc, pin,  # Pass PIN as string
                        name=name if name else None,
                        email=email if email else None,
                        new_pin=new_pin if new_pin else None
                    )
                    if "Successfully" in result:
                        show_message(result, "success")
                    else:
                        show_message(result, "error")
                except ValueError:
                    show_message("Invalid input.", "error")
            else:
                show_message("Please provide account number and current PIN.", "warning")

elif menu == "🗑️ Delete Account":
    st.markdown("## Delete Account")
    st.markdown("⚠️ **WARNING**: This action cannot be undone!")
    
    with st.form("delete_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            acc = st.text_input("🏦 Account Number", placeholder="Enter account number")
        
        with col2:
            pin = st.text_input("🔐 PIN", type="password", placeholder="Enter your PIN")
        
        confirm = st.checkbox("I understand this action cannot be undone")
        
        submitted = st.form_submit_button("Delete Account", use_container_width=True)
        
        if submitted:
            if not confirm:
                show_message("Please confirm you understand this action cannot be undone.", "warning")
            elif acc and pin:
                try:
                    result = Bank.delete_account(acc, pin)  # Pass PIN as string
                    if "successfully" in result:
                        show_message(result, "success")
                    else:
                        show_message(result, "error")
                except ValueError:
                    show_message("Invalid input.", "error")
            else:
                show_message("Please fill all fields.", "warning")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏦 SimpleBank - Secure Digital Banking Platform</p>
    <p style="font-size: 0.9rem;">Your data is stored locally and never shared with third parties.</p>
</div>
""", unsafe_allow_html=True)
