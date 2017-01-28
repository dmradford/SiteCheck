import Tkinter, SiteCheck, thread, tkMessageBox

def sitecheck():
    if SiteCheck.running == 0:
        SiteCheck.running = 1
        thread.start_new_thread(SiteCheck.run, ())
    else:
        tkMessageBox.showwarning("Scraper", "Scraper is already running")
        
def stopsitecheck():
    if SiteCheck.running == 2:
        SiteCheck.running = 1
    elif SiteCheck.running == 1:
        tkMessageBox.showwarning("Scraper", "Scraper is stopping")
    else:
        tkMessageBox.showwarning("Scraper", "Scraper is not currently running")
        
def emailsites():
    thread.start_new_thread(SiteCheck.emailsites, ())

top = Tkinter.Tk()

Tkinter.Button(top, text="Run Scraper", command = sitecheck).pack()
Tkinter.Button(top, text="Stop Scraper", command = stopsitecheck).pack()
Tkinter.Button(top, text="Email Site List", command = emailsites).pack()

top.mainloop()
