#!/usr/bin/python3

#to parse arguments
import argparse
import os
import yaml
import datetime
import time

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

# send a message
def send_message(host,port,send_account,pswd,to_account, hostname, status):
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

  # add in the actual person user to the message template
  user = str(os.getenv('USER'))

  # create a message
  msg = MIMEMultipart()

  # setup the parameters of the message
  msg['From']=send_account
  msg['To']=to_account
  msg['Subject']="SERVER STATUS"

  # get the message template and fill it up
  message_template = read_template('msg_status.txt')

  # send initial message
  date = str(datetime.datetime.now().date())
  time = str(datetime.datetime.now().time())

  message = message_template.substitute(USER=user, HOSTNAME= hostname, STATUS=status, DATE=date, TIME=time)
  # add in the message body
  msg.attach(MIMEText(message, 'plain'))
  # send the message via the server set up earlier.
  s.send_message(msg)
  del msg

# main app
def main(host,port,send_account,pswd,to_account,hostname,period):
  # init with status successful
  status = "ALIVE"
  send_message(host,port,send_account,pswd,to_account,hostname,status)

  # and then check the response
  while True:
    response = os.system("ping -c 1 " + hostname + " > /dev/null 2>&1")
    # check ping response
    if response == 0:
      new_status = "ALIVE"
    else:
      new_status = "DEAD"
    # if status changed, report
    if new_status != status:
      print("Server status changed to %s, trying to notify"%new_status)
      status = new_status
      send_message(host,port,send_account,pswd,to_account,hostname,status)
    # go to bed baby
    time.sleep(period)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser("Example of sending an email using python.")
    arg_parser.add_argument('--cfg','-c', type=str, default='cfg.yaml', help='email info config file. Defaults to \'%(default)s\'')
    arg_parser.add_argument('--server','-s', type=str, default='google.com', help='Server to check for life. Defaults to \'%(default)s\'')
    arg_parser.add_argument('--period','-p', type=int, default=60, help='Period in seconds to check for life. Defaults to \'%(default)s\'')
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
         cfg["to_account"],
         args.server,
         args.period)