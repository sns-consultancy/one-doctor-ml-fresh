import yagmail

def send_report(recipient_email: str, pdf_file: str):
    yag = yagmail.SMTP("your_gmail@gmail.com", "your_gmail_app_password")
    yag.send(
        to=recipient_email,
        subject="Your Health Report",
        contents="Attached is your One Doctor health prediction report.",
        attachments=pdf_file
    )
