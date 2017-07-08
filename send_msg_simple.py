#!/usr/bin/python3

#to parse arguments
import argparse
import os
import yaml

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
  try:
    s = smtplib.SMTP(host=host, port=port,timeout=1)
  except:
    print("connection unsuccessful. Exiting")
    exit()
  s.starttls()
  try:
    s.login(send_account,pswd)
  except:
    print("login unsuccessful. Exiting")
    exit()


  # get the message template and fill it up
  message_template = read_template('msg_simple.txt')

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
    arg_parser.add_argument('--cfg','-c', type=str, default='cfg.yaml', help='email info config file. Defaults to \'%(default)s\'')
    args = arg_parser.parse_args()

    # try to open the config file
    try:
      print("Trying to open config %s file"%args.cfg)
      f = open(args.cfg,'r')
      cfg = yaml.load(f)
      print("Using host: {}".format(cfg["host"]))
      print("Using port: {}".format(cfg["port"]))
      print("Using send_account: {}".format(cfg["send_account"]))
      print("Using pswd: {}".format(cfg["pswd"]))
      print("Using to_account: {}".format(cfg["to_account"]))
    except:
      print("Problem parsing files")
      quit()

    print("Successfully opened yaml file and got all content. Sending mail")
    main(cfg["host"],
         cfg["port"],
         cfg["send_account"],
         cfg["pswd"],
         cfg["to_account"])