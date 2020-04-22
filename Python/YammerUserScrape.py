# import time to enable delays, to wait for webpage loads; import selenium for automated web scripting
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

def getUsersFromYammer():
  # use Chrome as the webdriver; link to this driver here: https://sites.google.com/a/chromium.org/chromedriver/downloads

  locChrome = "C:\\Users\\roseqbr\\AppData\\Local\\WebDriver\\chromedriver.exe"
  driver = webdriver.Chrome(executable_path=locChrome)
  
  # navigate to Manulife SharePoint location
  initialLoginURL = "https://www.yammer.com/login?locale=en-US&locale_type=standard"
  driver.get(initialLoginURL)

  # provide [ID]@[org].com username
  Username = "[ID]@[org].com"

  # submit email address to the initial login page
  emailElement = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("login"))
  emailElement.send_keys(Username, Keys.ENTER)
  time.sleep(4)
  
  # note: for my organization, entering username into the login field redirects to an (automatic) authorization page
  # note: for a standard Yammer login, scripting a password entry may be required
  
  # store list of CRDs to use within URL strings (org specific CRDs 
    listOfYammerGroups = [16468991, 14402029, 17091096]
  
  # setup loop variables
  emailList = []
  userListCount = 0

  # navigate to a new link for each feedID on list
  for yammerGroup in listOfYammerGroups:
      
      # set up the initial variable to track if more pages are available
      moreAvailable = True

      # set up variable to track what current page in the URL string
      pageCount = 1


      while moreAvailable:
      
        # link to receive JSON format data for a given feedID
        url = "https://www.yammer.com/api/v1/users/in_group/{}.json?page={}".format(yammerGroup, pageCount)
        driver.get(url)

        # remove any HTML tags in the page with a regular expression
        tag_remove_re = re.compile(r'<[^>]+>')
        data = tag_remove_re.sub('', driver.page_source)

        # read remaining JSON format data
        jsonData = json.loads(data)
        
        # for each user, create an e-mail string using their name and email address (format is "[name] <[email]>")
        for u in jsonData['users']:
            emailList.append(u['full_name'] + " <" + u['email'] + ">")
        
        # count to go to the next available page
        pageCount += 1

        # if the JSON data indicates no more pages are available, set variable to false to break out of loop
        moreAvailable = jsonData['more_available']

        # allow two seconds to ensure the page is fully loaded prior to navigating to the next page
        time.sleep(2)
  
  emailList.sort()
  emailList = list(dict.fromkeys(emailList))

  print("----- Beginning of List -----")
  for email in emailList:
      print(email)
      userListCount += 1
  print("Total Number of Users: ", userListCount)  
    
  driver.close()    

getUsersFromYammer()
