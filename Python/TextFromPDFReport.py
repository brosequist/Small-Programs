from tika import parser
import urllib.request

# Objective, identify:
# 1) The Rep Name
# 2) If they are currently registered with a broker
# 3) If they were registered with Royal Alliance, their term date
# 4) A snapshot of their registration history

listOfCRDs = [215549
, 837692, 2042506, 5584134, 2409963, 1234
]

def validateRawContent(listOfCRDs):
    for CRD in listOfCRDs:
        # set URL
        url = "https://files.brokercheck.finra.org/individual/individual_{}.pdf".format(CRD)
        try:
            # open URL and convert to text with tika
            urlRequest = urllib.request.urlopen(url)
            raw = parser.from_buffer(urlRequest)
            print(raw)
            print(raw['content'])
        except:
            print("Cannot open {}".format(url))


validateRawContent(listOfCRDs)

def repRegistrationReport(listOfCRDs):

    print("############################## Start of Report #########################################")
    for CRD in listOfCRDs:
        # set URL
        url = "https://files.brokercheck.finra.org/individual/individual_{}.pdf".format(CRD)
        try:
            # open URL and convert to text
            urlRequest = urllib.request.urlopen(url)
            raw = parser.from_buffer(urlRequest)
            rawContent = raw['content']

            # First feature - identify rep name per PDF
            # Identify text prior to the rep name
            nameBlockBegin = rawContent.find("BrokerCheck Report")
            # Add expected buffer
            nameBlockBegin += 20
            # Identify text after rep name
            nameBlockEnd = rawContent.find("Section Title")
            # Subtract expected buffer
            nameBlockEnd -= 2
            # print(raw['content'][nameBlockBegin:nameBlockEnd])
            repName = rawContent[nameBlockBegin:nameBlockEnd]
            print("\nName: " + repName)
            
            # Second feature - identify if the broker is currently registered            
            if "This broker is not currently registered." in rawContent:
                print("Current Registration Status: Not registered")
            else:
                print("Current Registration Status: Registered")
            
            # Third feature - identify and display registration history
            # Find the beginning of registration history block
            dateBlockBegin = rawContent.find("The broker previously was registered with")
            # Find end of registration history block
            dateBlockEnd = rawContent.find("This section provides up to 10 years")
            # Offset to expected end of block
            dateBlockEnd -= 72
            
            registrationHistory = rawContent[dateBlockBegin:dateBlockEnd]
            
            # Sub feature - print term date from Royal Alliance if found
            # if the find function = -1, this means not found
            if registrationHistory.find("ROYAL ALLIANCE ASSOCIATES") != -1:
                # find beginning of text for Royal Alliance registration
                termDateEnd = registrationHistory.find("ROYAL ALLIANCE ASSOCIATES")
                # step back by one character to get to true end of date
                termDateEnd -= 1
                # step back by seven characters to get to beginning of date
                termDateBegin = termDateEnd - 7
                print("Term date from Royal Alliance: " + registrationHistory[termDateBegin:termDateEnd] + '\n')
            else:
                print()

            # print full registration history info
            print(registrationHistory,"\n")

        except:
            # in case
            print('Issue opening CRD: {}\nAt the following URL: {}'.format(CRD, url))
        
        print("########################################################################################")


repRegistrationReport(listOfCRDs)
