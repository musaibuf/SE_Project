import streamlit as st
from database import (
    setup_database, is_existing_user, save_user_to_db, get_user_data,
    is_existing_phone, get_username_by_phone, update_user_secret, update_user_password
)
from auth import generate_otp, send_otp_whatsapp, verify_otp

def forgot_password_page():
    """Page for users to reset their password."""
    st.title('Forgot Password')
    phone = st.text_input('Enter your registered phone number')
    if st.button('Send OTP'):
        username = get_username_by_phone(phone)
        if username:
            otp = generate_otp()
            update_user_secret(username[0], str(otp))
            send_otp_whatsapp(phone, otp)
            st.session_state['reset_username'] = username[0]
            st.success('OTP sent to your WhatsApp!')
        else:
            st.error('This phone number is not registered.')
            
def reset_password_page():
    """Page for users to enter OTP and new password."""
    st.title('Reset Password')
    if 'reset_username' not in st.session_state:
        st.warning("Please initiate the password reset process from the 'Forgot Password' page.")
        st.stop()
    otp_input = st.text_input('Enter OTP', type='password')
    new_password = st.text_input('Enter your new password', type='password')
    confirm_password = st.text_input('Confirm your new password', type='password')
    if st.button('Reset Password'):
        if not new_password or not confirm_password:
            st.error('Please enter and confirm your new password.')
        elif new_password != confirm_password:
            st.error('Passwords do not match.')
        else:
            user_data = get_user_data(st.session_state['reset_username'])
            if user_data and verify_otp(otp_input, user_data[1]):
                update_user_password(st.session_state['reset_username'], new_password)
                st.success('Your password has been reset successfully!')
                del st.session_state['reset_username']  # Clean up session state
            else:
                st.error('Invalid OTP. Please try again or re-initiate the password reset process.')

            
def signup_page():
    """Page for users to sign up."""
    st.title('Signup Page')
    username = st.text_input('Enter Username')
    password = st.text_input('Enter Password', type='password')
    phone = st.text_input('Enter Phone Number')
    if st.button('Sign Up'):
        if not username or not password or not phone:
            st.error('Please fill in all fields.')
        elif is_existing_user(username):
            st.error('Username already exists.')
        elif is_existing_phone(phone):
            st.error('Phone number already used.')
        else:
            otp = generate_otp()
            save_user_to_db(username, password, phone, str(otp))
            send_otp_whatsapp(phone, otp)
            st.success('Signup successful! Check your WhatsApp for the OTP to complete your registration.')

def login_page():
    """Page for users to log in."""
    st.title('Login Page')
    username = st.text_input('Username')
    otp_input = st.text_input('OTP', type='password')
    if st.button('Login'):
        user_data = get_user_data(username)
        if user_data and verify_otp(otp_input, user_data[1]):  # Access secret using index 1
            st.success('Login successful!')
        else:
            st.error('Login failed. Invalid username or OTP.')

def main():
    """Main function to navigate between pages."""
    setup_database()
    st.sidebar.title('Navigation')
    page_selection = st.sidebar.radio("Choose a page:", ['Signup', 'Login', 'Forgot Password'])
    
    if page_selection == 'Signup':
        signup_page()
    elif page_selection == 'Login':
        login_page()
    elif page_selection == 'Forgot Password':
        forgot_password_page()
        if 'reset_username' in st.session_state:
            reset_password_page()

if __name__ == '__main__':
    main()