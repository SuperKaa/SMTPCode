import smtplib
import email.message
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

def send_otp_and_verify(emailadd):
    load_dotenv()

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    port = int(os.getenv("PORT"))

    otp = str(random.randint(100000, 999999))
    otp_creation_time = datetime.now()

    # creates email
    msg = email.message.EmailMessage()
    msg['From'] = sender_email
    msg['To'] = emailadd
    msg['Subject'] = "Your One-Time Password (OTP)"

    # html part
    html_content = f"""
    <html>
        <body>
            <h1 style="color: #4CAF50;">Your One-Time Password (OTP)</h1>
            <p>Your OTP is: <strong style="font-size: 20px; color: #2196F3;">{otp}</strong></p>
            <p>This OTP is valid for <strong>5 minutes</strong>.</p>
            <p>If you did not request this OTP, please ignore this email.</p>
            <hr>
            <p style="font-size: 12px; color: #888;">This is an automated message. Please do not reply.</p>
        </body>
    </html>
    """

    # add the html to the email
    msg.add_alternative(html_content, subtype="html")

    try:
        # send it
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("OTP sent successfully! Check your email.")
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return False

    # get otp from user
    user_otp = input("Enter the OTP you received: ").strip()  # Get OTP from user

    # check if its expired
    current_time = datetime.now()
    time_difference = current_time - otp_creation_time
    if time_difference > timedelta(minutes=5):
        print("OTP has expired.")
        return False

    # check if otp is correct
    if user_otp == otp:
        return True  # return true if otp matches
    else:
        return False  # return false if incorrect
    
#example

emailadd = input("Enter your email address: ")

while True:
    if send_otp_and_verify(emailadd):
        print("OTP verified")
        break
    else:
        print("OTP verification failed, please try again.")
