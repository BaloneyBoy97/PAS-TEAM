import smtplib
from email.mime.text import MIMEText

def send_test_email():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'AirViewSLU5030@gmail.com'
    smtp_password = 'byai nwlp euwb dufs'
    sender_email = 'AirViewSLU5030@gmail.com'
    recipient_email = 'zanxiang.wang@outlook.com'
    
    msg = MIMEText('This is a test email from the integration test.')
    msg['Subject'] = 'Test Email'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print('Test email sent successfully')
    except Exception as e:
        print(f'Failed to send test email: {e}')

if __name__ == '__main__':
    send_test_email()