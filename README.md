SimpleBank – Digital Banking Simulator
SimpleBank is a lightweight, browser-based digital banking simulation built with Python and Streamlit. It demonstrates core banking operations—account creation, deposits, withdrawals, account management, and deletion—all within a secure, locally stored environment. Ideal for learning full-stack Python web apps, local data management, and UI/UX design basics.

Features
Create Account: Open a new bank account with name, age, email, and a secure 4-digit PIN.

Deposit Money: Add funds to your account, with real-time balance updates and transaction limits.

Withdraw Money: Securely withdraw cash, with balance checks to prevent overdrafts.

View Account Details: See your profile, account number, and current balance in a clean, card-based layout.

Update Account: Change your name, email, or PIN as needed.

Delete Account: Permanently remove your account (action cannot be undone).

Responsive UI: Modern, mobile-friendly interface with custom styling and intuitive navigation.

Local Data Storage: All account data is saved in a local data.json file—no external databases or cloud storage.

Security: PINs are never displayed, and sensitive operations require authentication.

Quick Start
Install Dependencies

text
pip install streamlit
Run the App

text
streamlit run app.py
Open in Browser

The app will launch in your default browser at http://localhost:8501.

How It Works
Backend: Python manages account data (stored in data.json), generates unique account numbers, enforces validation rules, and handles all banking logic.

Frontend: Streamlit provides the web interface, with forms for each operation and visual feedback (success/error messages, animated confetti on account creation).

Data Security: All data remains on your machine. No information is shared externally.

Usage Guide
Create an Account: Enter your details and set a 4-digit PIN. You’ll receive a unique account number.

Deposit/Withdraw: Authenticate with your account number and PIN, then specify the amount.

View/Update Details: Access and modify your account information at any time.

Delete Account: Confirm your intention—this action is irreversible.

Security Note: Never share your PIN. All data is stored locally and is not recoverable if deleted.

Customization
UI Styling: Modify st.markdown CSS blocks to change colors, gradients, cards, and messages.

Data File: By default, data is saved to data.json in your working directory. Change the filename in the Bank class if needed.

Transaction Limits: Adjust the maximum deposit/withdrawal amounts directly in the deposit_money and withdraw_money methods.

Requirements
Python 3.7+

Streamlit (pip install streamlit)

Limitations
Local Storage: Data is not synced across devices and is vulnerable if the data.json file is deleted or corrupted.

Scalability: Designed for personal or educational use, not for production or large-scale deployment.

No Interest/History: Basic simulation only—no transaction history, interest calculation, or advanced banking features.

Contributions
This project is open for learning and experimentation. Feel free to fork, extend, or adapt it for your needs. Suggestions and pull requests are welcome!

About
SimpleBank is a demo project for educational and prototyping purposes. It is not affiliated with any real financial institution and does not handle real money.
