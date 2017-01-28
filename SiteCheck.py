import scraper, os, smtplib, time, re, datetime, ast

#####################
#### Definitions ####
#####################

def initfiles(): # Create data files if none exist
    for i in range(len(activesites)):
        try:
            if os.path.isfile("sites\\"+activesites[i][0]+".dat") == False:
                open("sites\\"+activesites[i][0]+".dat", "w").write("")
                open("sites\\"+activesites[i][0]+"_OLD.dat", "w").write("")
        except:
            None
        
def check(): # Saves current data from the website
    for i in range(len(activesites)):
        try:
            scraper.conNum = activesites[i][1]
            scraper.ImportURL = activesites[i][2]
            scraper.importquery(scraper.conNum, scraper.ImportURL, activesites[i][0])
        except:
            None

def ttOld(): # Copies old data to _OLD file
    for i in range(len(activesites)):
        try:
            if open("sites\\"+activesites[i][0]+"_OLD.dat").read() != open("sites\\"+activesites[i][0]+".dat").read():
                open("sites\\"+activesites[i][0]+"_OLD.dat", "w").write(open("sites\\"+activesites[i][0]+".dat").read())
        except:
            None
        
def compare(): # Compares _OLD files to current ones.
    newposts = []
    for i in range(len(activesites)):
        try:
            f1 = open("sites\\"+activesites[i][0]+".dat").read()
            f2 = open("sites\\"+activesites[i][0]+"_OLD.dat").read()
            f1L = [a[1:-1] for a in re.findall('".+?"', f1)]
            f2L = [a[1:-1] for a in re.findall('".+?"', f2)]
            p1 = f1L[0]
            for x in range(len(f1L)):
                try: f1L.remove(p1)
                except: break
            for y in range(len(f2L)):
                try: f2L.remove(p1)
                except: break
            #print ("f1L: "+str(f1L)+"\n")
            #print ("f2L: "+str(f2L)+"\n")
            nomatch = [x for x in f1L if x not in f2L]
            print ("Non matching"+str(nomatch))
            nomatchkey = []
            for z in range(len(nomatch)):
                for w in range(len(keys)):
                    if keys[w].lower() in nomatch[z].lower():
                        nomatchkey.append(nomatch[z])
            newposts.append([activesites[i][0], nomatchkey])
            print ("Non matching with keyword"+str(nomatchkey)+", length: "+str(len(nomatchkey)))
            try:
                if len(nomatchkey)==0:
                    print (activesites[i][0]+" No new matching posts")
                else:
                    changedsites.append((activesites[i][0]))
            except: None
        except: None

def sendmail(sites): # Configurarion for sending email
    FROMADDR = emailconfig['From'].strip("\n")
    LOGIN    = emailconfig['Login'].strip("\n")
    PASSWORD = emailconfig['Password'].strip("\n")
    TOADDRS  = [emailconfig['To'].strip("\n")]
    SUBJECT  = "Website has changed"

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
    msg += str(sites)
    if emailconfig['SSL'].strip("\n") == 'True':
        print ("Using SSL")
        server = smtplib.SMTP_SSL(emailconfig['Server'].strip("\n"), int(emailconfig['Port'].strip("\n")))
    else:
        server = smtplib.SMTP(emailconfig['Server'].strip("\n"), int(emailconfig['Port'].strip("\n")))
    server.set_debuglevel(1)
    server.ehlo()
    try:
        server.starttls()
    except:
        print ("Not using starttls")
    server.login(LOGIN, PASSWORD)
    server.sendmail(FROMADDR, TOADDRS, msg)
    server.quit()

def nameurl(name): # Return name and URL from sitelist
    with open('sitelist.txt') as myFile:
        for num, line in enumerate(myFile, 1):
            if name in line:
                pair = name+"\n"+open('sitelist.txt').readlines()[num+1]
                return pair

def defbody(l): # Return concatenated list of changed websites
    emailbody = ''
    for i in range(len(l)):
        emailbody = emailbody+"\n\n"+nameurl(l[i])
    return emailbody

##def checklog():
##    log = ast.literal_eval(open("sites\\log.dat").read())
##    for i in activesites:
        
    
################################
#### Load and create inputs ####
#### Create empty variables ####
################################
   
sitelist = open("sitelist.txt").read().split("\n\n")
sitelist = [x for x in sitelist if x is not '']
log = {} # Empty dict for holding log information
emailconfig = {} # Empty dict for emailconfig
with open("emailconfig.txt") as f: # Import email config data into emailconfig dict
    for line in f:
        (key, val) = line.split(": ")
        emailconfig[key] = val
activesites = [] # Empty list for active sites to contain list of lists for active websites
for i in range(len(sitelist)): # Append sitelist to activesites
    activesites.append(sitelist[i].split("\n"))
changedsites = [] # Empty list for websites that have changed since last check
keys = open("keywords.txt").read().split("\n") # Import keywords from file, split return into list
newposts = [] # Empty list for holding new posts
running = 0 # Used in run() to denote if SiteCheck is ready to start, starting/stopping, or running

###########################
#### Create Base Files ####
###########################
    
initfiles()

######################################
#### Check and email continuously ####
######################################

def run(): # Check for changes and email list
    global running
    global changedsites
    if running == 1:
        running = 2
    while running == 2:
        st1 = time.clock()
        starttime = time.clock()
        ttOld()
        check()
        endtime = time.clock()
        print (endtime-starttime)
        changedsites.append(compare())
        changedsites = [x for x in changedsites if x is not None]
        if changedsites != []:
            emailbody = "The following websites have been changed within the last 3 minutes:\n"+defbody(changedsites)
            sendmail(str(emailbody))
            changedsites = []
            emailbody = ''
        endtime = time.clock()
        print ("Gathering data took "+str(endtime-starttime)+" to complete")
        #time.sleep((60)-(endtime-starttime))
        et1 = time.clock()
        print ("Entire Process took "+str(et1-st1)+" to complete")
    running = 0

def emailsites(): # Email list of currently active sites
    em = []
    for i in range(len(activesites)-1):
        em.append(activesites[i][0])
    emailbody = "Here is a list of all currently active sites:\n"+defbody(em)
    sendmail(str(emailbody))
    changedsites = []
    emailbody = ''
