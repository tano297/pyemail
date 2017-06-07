#!/usr/bin/python3

#to parse arguments
import argparse
import os

#template to parse email message
from string import Template

#to handle smtp connections we need smtplib
import smtplib

#to work with email sending
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#function to read in the template from the message
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

# main app
def main(host,port,send_account,pswd,to_account):
  # set up the SMTP server
  s = smtplib.SMTP(host=host, port=port)
  s.starttls()
  s.login(send_account,pswd)

  # get the message template and fill it up
  message_template = read_template('msg.txt')

  # create a message
  msg = MIMEMultipart()

  # add in the actual person user to the message template
  user = os.getenv('USER')
  message = message_template.substitute(USER=user)

  # setup the parameters of the message
  msg['From']=send_account
  msg['To']=to_account
  msg['Subject']="Tada!"

  # add in the message body
  msg.attach(MIMEText(message, 'plain'))

  # send the message via the server set up earlier.
  s.send_message(msg)
  del msg

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser("Example of sending an email using python.")
    arg_parser.add_argument('--host', type=str, default='smtp-mail.outlook.com', help='smtp server name. Defaults to \'%(default)s\'')
    arg_parser.add_argument('--port', type=int, default=587, help='smtp server port number. Defaults to \'%(default)s\'')
    arg_parser.add_argument('--send_account', type=str, default="tano.297@hotmail.com", help='account to send email from. Defaults to \'%(default)s\'')
    arg_parser.add_argument('--pswd', type=str, default="", help='password for the account to send email from. Defaults to \'%(default)s\'')
    arg_parser.add_argument('--to_account', type=str, default="tano.297@gmail.com", help='account to send email to. Defaults to \'%(default)s\'')    
    args = arg_parser.parse_args()


    main(args.host,
         args.port,
         args.send_account,
         args.pswd,
         args.to_account)




