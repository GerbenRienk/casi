'''
Created on 11 apr. 2017

@author: GerbenRienk
'''


# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from utils.dictfile import readDictFile
config=readDictFile('oli.config')


def MailThisLogFile(LogFileName):
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    with open(LogFileName) as fp:
        # Create a text/plain message
        msg = MIMEText(fp.read())
    
    msg['Subject'] = config['mail_subject']
    msg['From'] = config['mail_from']
    msg['To'] = config['mail_to']
    
    # Send the message via our own SMTP server,
    # but only if we can send mails
    if config['mail_enabled'].lower() == "true":
        mail_server = smtplib.SMTP(config['mail_server'])
        mail_server.send_message(msg)
        mail_server.quit()
    else:
        print("mail not enabled")
        print(msg)
        
if __name__ == '__main__':
    MailThisLogFile('logs/report.txt')