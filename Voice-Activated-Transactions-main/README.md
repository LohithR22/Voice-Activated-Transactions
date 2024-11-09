# **Voice-Activated UPI Transaction System**

## Project Overview

The **Voice-Activated UPI Transaction System** is an innovative solution designed to streamline UPI transactions using voice commands. Built with Python, Streamlit, and SQLite, this project enables secure transactions through a user-friendly interface. It supports functionalities like user login, transaction processing, balance management, and account handling, all controlled through voice commands.

This project demonstrates the integration of voice commands with financial technology in a localized setup, serving as a prototype for further expansion into real-world applications.

## Features

- **Secure Login System**: Users log in with a username and password. Credentials are validated against an SQLite database.
- **Voice-Activated Transactions**: Users record a voice command to initiate transactions, which is then transcribed, parsed, and validated before updating balances.
- **Add/Delete User**: Admins can add or remove accounts with unique usernames, passwords, and initial balances.
- **Interactive Frontend**: Built with Streamlit, providing an easy-to-use UI with balance updates and transaction confirmations in real-time.

## System Requirements

- **Python 3.8** or higher
- **Python Libraries**:
  - `streamlit`
  - `sqlite3` (built-in with Python)
  - `speechrecognition` (for optional voice-to-text)

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd voice-activated-upi-transaction

2. **Install Required Libraries**
   ```bash
   pip install streamlit speechrecognition
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Testing Voice Commands**
   - Simulated transcription is used in the absence of a live voice-to-text API.
   - Direct text input can be used for testing transactions.

## Project Structure

- **app.py**: Manages the Streamlit UI, including login, transaction processing, and account management.
- **backend.py**: Handles database operations, including user validation, balance updates, and transaction processing.
- **transcriber.py**: (optional) For audio recording and transcription if connected with a voice-to-text API.

## Code Explanation

### backend.py

This file contains database operations such as:
- **Database Initialization**: Sets up SQLite with predefined users.
- **User Validation**: Verifies login credentials.
- **Transaction Processing**: Deducts the specified amount from the sender’s balance and credits it to the receiver.
- **Balance Retrieval**: Displays the user’s balance before and after each transaction.

### app.py

This file includes the Streamlit-based frontend:
- **Login System**: Secure login with predefined credentials.
- **Transaction Interface**: Allows voice recording and transcription for transactions.
- **Add/Delete User**: Enables user management directly through the UI.
- **Balance Display**: Shows “Balance Before Transaction” and “Balance After Transaction” for clarity.

## Example Workflow

1. **Login**: Users enter their username and password.
2. **Balance Display**: Current balance appears upon login.
3. **Transaction Processing**:
   - Click "Start Recording" to record a transaction command.
   - Click "Stop Recording and Transcribe" to transcribe the audio command.
4. **Account Management**: Users can add a new account or delete an existing account.
5. **Logout**: Single-click logout to return to the main login page.

## Known Limitations

- **User Base**: Limited to predefined users.
- **Voice-to-Text Accuracy**: Limited without a live transcription API.
- **Security**: Lacks encryption for stored passwords.

## Future Enhancements

1. **Real-Time Voice-to-Text Integration**: Integrate a live voice recognition API.
2. **Enhanced Security**: Implement encryption for credentials.
3. **Scalability**: Expand database capacity for larger user bases.

## Conclusion

The **Voice-Activated UPI Transaction System** is a functional prototype demonstrating the use of voice commands for financial transactions. While designed for a local environment, it can be scaled and secured for broader applications in the fintech industry, with potential integrations for real-time voice APIs and advanced security measures.
```
