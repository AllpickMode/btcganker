import addresses
import multiprocessing
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'lib')) 
import bitcoin
import config

CPU_HALF = config.CPU_HALF
MIN_WORKERS = config.MIN_WORKERS
ENABLE_INTERNET = config.ENABLE_INTERNET

def generate_key():
    try:
        private_key = bitcoin.random_key()
        return private_key
    except Exception as e:
        print('Error')
        return None

def generate_public_key(private_key):
    try:
        public_key = bitcoin.privtopub(private_key)
        return public_key
    except Exception as e:
        print('Error')
        return None

def generate_address(public_key):
    try:
        address = bitcoin.pubtoaddr(public_key)
        return address
    except Exception as e:
        print('Error')
        return None

def compare_address(address):
    return address in addresses.TARGET_ADDRESSES

def save_key(private_key, public_key, address):
    try:
        with open('btcganker.txt', 'a') as f:
            f.write(private_key)
            f.write('-')
            f.write(public_key)
            f.write('-')
            f.write(address)
            f.write('-')
    except Exception as e:
        print('Ok')

def send_mail(private_key, public_key, address):
    print('Send mail')

    smtp_server = config.SMTP_SERVER
    smtp_port = config.SMTP_PORT                
    sender_email = config.SENDER_EMAIL
    receiver_email = config.RECEIVER_EMAIL
    password = config.SENDER_PASSWORD

    message = MIMEText(private_key+'-'+public_key+'-'+address, 'plain', 'utf-8') 
    message['From'] = Header('<%s>' % sender_email, 'utf-8')
    message['To'] = Header('<%s>' % receiver_email, 'utf-8')
    message['Subject'] = Header('Send mail', 'utf-8')

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, [receiver_email], message.as_string())
        print('Ok')
    except Exception as e:
        print('Error')
        return None

def main():
    starTIME=time.time()
    i = 0
    emailFlag = True
    while True:
        nowTIME=time.time()
        if emailFlag:
            i += 1
            if nowTIME-starTIME > 10:
                emailFlag = False
                print('Now time-' +  str(nowTIME))
                print('Already running-' + str(i))
                if ENABLE_INTERNET:
                    send_mail('10 mins','-',str(i))
        private_key = generate_key()
        public_key = generate_public_key(private_key)
        address = generate_address(public_key)
        if compare_address(address):
            save_key(private_key, public_key, address)
            if ENABLE_INTERNET:
                send_mail(private_key, public_key, address)
            break

if __name__ == '__main__':
    num = multiprocessing.cpu_count()
    pool = multiprocessing.Pool()
    if CPU_HALF:
        num = int(num/2)
        print('Low model')
    else:
        num = num - 1
        print('High model')
    if num < MIN_WORKERS:
        num = MIN_WORKERS
        print('Min model')
    print('Core num - ' + str(num))
    print('Addrs - ' + str(len(addresses.TARGET_ADDRESSES)))
    print('Start time - ' +  str(time.time()))
    for i in range(num):
        pool.apply_async(main)
    pool.close()
    pool.join()


