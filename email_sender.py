import smtplib


def send_email(address_input):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('huangbo@bu.edu','HBXboris99!')
    server.sendmail('huangbo@bu.edu', '{}'.format(address_input),'You are my guest now!')

if __name__ == '__main__':
    email = input("Please enter your email address:")
    send_email(email)