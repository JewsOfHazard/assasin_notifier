import smtplib
import sys
import argparse

def smtp_connect(gmail_sender, gmail_passwd):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    return server

def send_email(server, gmail_sender, destination_numbers, email_list, message):

    for entry in destination_numbers:
        for email in email_list:
            TEXT = message
            TO = entry + email
            BODY = '\r\n'.join(['To: %s' % TO, 'From: %s' % "Assasin Notifier", 'Subject: %s' % "",'', TEXT])
            print("Sending email to {} through the email {}".format(entry, email))
            server.sendmail(gmail_sender, [TO], BODY)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument("-n", "--number", nargs='?', help="The number to test sending to.")
    parser.add_argument("-m", "--message", nargs='?', default="Logan forgot to add a message and he is stupid.", help="The message to send.")

    args = parser.parse_args()

    verizon_email = "@vtext.com"
    tmobile_email = "@tmomail.net"
    sprint_email = "@messaging.sprintpcs.com"
    att_email = "@txt.att.net"

    email_list = [verizon_email, tmobile_email, sprint_email, att_email]

    gmail_details = []

    with open("smtp_login.txt", "r+") as login_info:
        for i in login_info:
            gmail_details.append(i)

    gmail_sender, gmail_passwd = gmail_details[0], gmail_details[1]

    server = smtp_connect(gmail_sender, gmail_passwd)

    user_contacts = []

    with open("phone_numbers.txt", "r+") as opened:
        for line in opened:
            if line[0] != "#":
                user_contacts.append(line.rstrip())

    if args.number == None:
        send_email(server, gmail_sender, user_contacts, email_list, args.message)
    else:
        send_email(server, gmail_sender, [args.number], email_list, args.message)

    server.quit()
