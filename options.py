class BomberOptions(object):
    def __init__(self) -> None:
        self.__victim_address = ""
        self.__email_subject = ""
        self.__email_body = ""
        self.__email_amount = 0
        self.__attacker_gmail_address = ""
        self.__attacker_gmail_password = ""
        self.__attacker_anonymous_name = ""
        
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
        
    @property
    def email_body(self) -> str:
        return self.__email_body
    
    @email_body.setter
    def email_body(self, body: str) -> None:
        self.__email_body = body
        
    @property
    def email_amount(self) -> str:
        return self.__email_amount
    
    @email_amount.setter
    def email_amount(self, amount: str) -> None:
        try:
            self.__email_amount = int(amount)
        except (TypeError, ValueError):
            raise ValueError('The email amount must be a number')
        
    @property
    def attacker_gmail_address(self) -> str:
        return self.__attacker_gmail_address
    
    @attacker_gmail_address.setter
    def attacker_gmail_address(self, address: str) -> None:
        if not self.__is_email_address(address):
            raise ValueError('Please enter a valid attacker email address')
        self.__attacker_gmail_address = address
        
    @property
    def attacker_gmail_password(self) -> str:
        return self.__attacker_gmail_password
    
    @attacker_gmail_password.setter
    def attacker_gmail_password(self, password: str) -> None:
        self.__attacker_gmail_password = password
        
    @property
    def attacker_anonymous_name(self) -> str:
        return self.__attacker_anonymous_name
    
    @attacker_anonymous_name.setter
    def attacker_anonymous_name(self, name: str) -> None:
        self.__attacker_anonymous_name = name
        
    def __is_email_address(self, address: str) -> bool:
        if address.find('@') == -1:
            return False
        return address.split('@')[1].find('.') == -1
