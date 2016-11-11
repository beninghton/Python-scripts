#!/usr/bin/python
import re
import subprocess
import os
import smtplib
import copy
import paramiko
import sys

serv1="serv1_ip_addr"
serv2="serv2_ip_addr"
serv3="serv3_ip_addr"
mailuser="yourmailuser"
mailpwd="yourmailpass"
recipient="beninghton6@yandex.ru"
subject="ALL IS BAD!"
sshuser="yoursshuser"
sshpass="yoursshpass"

servers = [serv1,serv2,serv3]

def send_email(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"        

def ssh_connect(servername,username, password, command):
    
    	server=servername
    	user= username
    	pwd = password
    	comm = command
    	ssh = paramiko.SSHClient()
    	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    	ssh.connect(server, username=user, password=pwd)
    	stdin, stdout, stderr = ssh.exec_command(comm)
    	output = copy.deepcopy(stdout.read())
    	ssh.close()
    	return output      
 
body = ''
problem = 0

for server in servers:
    try:
    	output = ssh_connect(server,sshuser,sshpass,"df -h")    
    except:
	print "can't connect over ssh to server "+server
        sys.exit()  	
    for line in output.split("\n"):
        if ("99%" in line or "100%" in line) and ("/dev/" in line):
            disk = re.search(r'.+\d\s', line).group(0)
            body = body+"Na servere "+server+", diske "+disk+"Vse ploho!\n"
            problem = 1
        

if problem!=0:
    send_email(mailuser, mailpwd, recipient, subject, body)
    problem = 0

