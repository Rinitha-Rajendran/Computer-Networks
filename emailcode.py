import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def sendemail(toemail, subject, body, imagpath=None):
    fromemail = 'Your email id'
    password = 'your password'  # Consider using environment variables for security
    msg = MIMEMultipart()
    msg['From'] = fromemail
    msg['To'] = toemail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    if imagpath:
        with open(imagpath, 'rb') as img:
            imagdata = MIMEImage(img.read())
            imagdata.add_header('Content-ID', '<image>')
            msg.attach(imagdata)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(fromemail, password)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")