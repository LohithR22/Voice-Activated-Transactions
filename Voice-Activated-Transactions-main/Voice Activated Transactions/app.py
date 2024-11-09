import streamlit as st
from transcriber import record_audio, transcribe_audio
from backend import initialize_db, process_transaction, validate_login, add_user, delete_user, get_balance

# Initialize the database
initialize_db()

# Streamlit app UI
st.title("Voice-Activated UPI Transactions")
st.write("Voice commands to make payments and clear bills.")

# Session state to manage login and add user state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "show_add_user" not in st.session_state:
    st.session_state.show_add_user = False
if "user_added" not in st.session_state:
    st.session_state.user_added = False
if "current_balance" not in st.session_state:
    st.session_state.current_balance = 0

# Toggle Add User Section
if st.session_state.show_add_user and not st.session_state.user_added:
    st.subheader("Add a New User")
    new_username = st.text_input("New User's Name (Username)", key="new_username")
    new_password = st.text_input("Password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    new_balance = st.number_input("Initial Balance", min_value=0, key="new_balance", step=100)

    # Validate Password Confirmation and Add User
    if st.button("Confirm Add User"):
        if new_username and new_password and confirm_password:
            if new_password == confirm_password:
                add_user(new_username, new_balance, new_username, new_password)
                st.success(f"User '{new_username}' added successfully!")
                st.session_state.user_added = True  # Prevent re-showing add user form
            else:
                st.error("Passwords do not match. Please try again.")
        else:
            st.error("Please fill out all fields.")

    if st.button("Cancel"):
        st.session_state.show_add_user = False

elif not st.session_state.logged_in:
    # Login Section
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_name = validate_login(username, password)
        if user_name:
            st.session_state.logged_in = True
            st.session_state.user_name = user_name
            st.session_state.user_added = False  # Reset add user form state on login
            st.session_state.current_balance = get_balance(user_name)  # Fetch current balance
            st.success(f"Logged in as {user_name}")
        else:
            st.error("Invalid username or password")

    if st.button("Add User"):
        st.session_state.show_add_user = True

# Main Transaction Section for Logged-in Users
if st.session_state.logged_in:
    st.subheader(f"Welcome, {st.session_state.user_name}")

    # Display Current Balance
    st.write(f"Current Balance: {st.session_state.current_balance} Rs")

    # Transaction Interface
    if st.button("Start Recording"):
        audio = record_audio()
        st.session_state.audio = audio
        st.write("Recording completed.")

    if st.button("Stop Recording and Transcribe"):
        if "audio" in st.session_state:
            transcription = transcribe_audio(st.session_state.audio)
            st.write("Transcription:", transcription)
            
            # Process transaction and handle non-existing receiver
            result, balance_before, balance_after = process_transaction(transcription, st.session_state.user_name)
            st.write(result)
            
            # Check if transaction was successful or receiver was missing
            if balance_before is not None and balance_after is not None:
                # Display balance information in a neat format
                st.write("**Balance Before Transaction:**")
                st.info(f"{balance_before} Rs")
                
                st.write("**Balance After Transaction:**")
                st.success(f"{balance_after} Rs")
                
                # Update the current balance after transaction
                st.session_state.current_balance = balance_after
            else:
                st.warning("Please re-record the transaction with a valid recipient.")
        else:
            st.write("No audio recorded. Please record first.")

    # Delete Account
    if st.button("Delete My Account"):
        delete_user(st.session_state.user_name)
        st.success("Your account has been deleted.")
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.current_balance = 0
        st.experimental_rerun()  # Immediately refresh to show login page after deletion

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.current_balance = 0
        st.experimental_rerun()  # Immediately refresh to show login page after logout
