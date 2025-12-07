import smtplib
from email.message import EmailMessage

# Email configuration
sender = "@gmail.com"
receiver = "recipient_email@gmail.com"
password = "your_app_password"  # Use an "App Password" for Gmail

# Create email
msg = EmailMessage()
msg["Subject"] = "Test Email from Python"
msg["From"] = sender
msg["To"] = receiver
msg.set_content("Hello, this is a test email sent using Python!")

# Send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(sender, password)
    smtp.send_message(msg)

print("Email sent successfully!")