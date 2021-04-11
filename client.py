from smtplib import SMTP as Client 
import smtplib

s = Client('localhost', 8025) 
try:
    s.set_debuglevel(True)
    s.sendmail('andy@example.com', ['bob@example.com'], """\
    Date:17/05/2017,2:18
    From: andy@example.com
    To: bob@example.com
    Subject: A test
    testing
    """)
    s.quit()
except smtplib.SMTPException:
    print("Error: unable to send email")
    import traceback
    traceback.print_exc()
