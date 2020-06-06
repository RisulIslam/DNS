import tkinter as tk
from win10toast import ToastNotifier
import time
import pandas as pd
import matplotlib.pyplot as plt

"""
This class is to maintain all the issues related to
notification (sending, schedling etc)
"""
class Notification():
    def __init__(self):
        self.toaster = ToastNotifier()
        

    """
        Input: takes a message
        Output: Send notification with that message
        package used: win10toast
    """
    def send_notification(self,message):
         self.toaster.show_toast("Alarm!!!!!", # header of the notification box
                   message,                    # Body of the notification
                   icon_path=None,
                   duration=4,                 # Duration of showing the notification
                   threaded=True)              # allowing all the other jobs while showing notification
        

class Settings():
    
    def __init__(self):
        self.__glass = 200                       # amount of water to be drunk everytime
        self.__totalQ = 2600                     # Total amount of water needed to drink
        self.__notify_interval=2*3600            # the time interval at which the notification will be send
        self.__totaltoday=0                      # Cumulative amount of water drunk today

    # set new glass size
    def set_glass(self,g):
        self.__glass = g

    # set new total amount    
    def set_totalQ(self,t):
        self.__totalQ = t
        
    # set new notification interval    
    def set_notify_interval(self,n):
        self.__notify_interval = n

    # set cumulative cnsumed water
    def set_totaltoday(self,tt):
        self.__totaltoday = tt


    # Get the private variables
    def get_glass(self):
        return self.__glass
        
    def get_totalQ(self):
        return self.__totalQ
        
    def get_notify_interval(self):
        return self.__notify_interval

    def get_totaltoday(self):
        return self.__totaltoday




class Aggregation():
    def __init__(self):
        self.a = 1


    """
        Input: None
        Output: Barplot of the consumed water for the last 7 days
        Plot package: matplotlib
    """
    def showstat(self):
        df = pd.read_csv("log.csv")                     # Read the log file
        df=df[-7:]
        amounts=df['amount']
        dates = df['date']
        
        plt.bar(dates,amounts)                          # Plot the bars
        plt.axhline(y=2600,color='g',linestyle='--')
        plt.xticks(rotation=20)
        plt.xlabel("Lat 7 Days")
        plt.xlabel("Water Consumed (ml)")
        plt.show()

        


"""
This class is the driver class. It is responsible to
    (i) Draw, maintain the frame
    (ii) Calling for sending notification
    (iii) Generate warning if about to consume less water
    (iv) Change the current settings
    (v) Call for Showing the stats
"""
class App():
    def __init__(self,window,notification, setting):
        self.notifications = notification
        self.settings = setting

        

        
        self.root = window
        self.root.title("My DNS")
        
        self.labelg = tk.Label(self.root,text="Set the glass size(ml): ")
        self.labelg.grid(row=1,column=0,sticky='W')

        self.varglass = tk.StringVar()
        self.varglass.set("200")
        self.OptionMenuentryg=tk.OptionMenu(self.root,self.varglass,"100","200","500","1000") # Option for changing glass size
        self.OptionMenuentryg.grid(row=1,column=1,sticky='W')


        
        self.labelt = tk.Label(self.root,text="Set the total amount(ml): ")
        self.labelt.grid(row=2,column=0,sticky='W')
        self.vartotal = tk.StringVar()
        self.vartotal.set("2600")
        self.OptionMenuentryt=tk.OptionMenu(self.root,self.vartotal,"2600","3600") # Option for changing from male to female consumption
        self.OptionMenuentryt.grid(row=2,column=1,sticky='W')


        
        self.labeln = tk.Label(self.root,text="Set the notification interval(sec): ")
        self.labeln.grid(row=3,column=0,sticky='W')
        self.varnotiinterval = tk.StringVar()
        self.varnotiinterval.set("7200")
        self.OptionMenuentryn=tk.OptionMenu(self.root,self.varnotiinterval,"1800","3600","7200","10") # Option for changing notification interval
        self.OptionMenuentryn.grid(row=3,column=1,sticky='W')
        
        self.buttonsetting = tk.Button(self.root,text="Change Settings",width = 12, command=self.clicksettings) # button for change settings
        self.buttonsetting.grid(row = 4,column=1,sticky="W")

        self.addwater_text = "You have drunk "+str(self.settings.get_totaltoday())+"/"+str(self.settings.get_totalQ())+" today."
        self.texttotaltoday = tk.Text(self.root,width=25, height=4, wrap = tk.WORD, background="white")
        self.texttotaltoday.grid(row=6,column=0,sticky='W')

        self.buttonaddwater = tk.Button(self.root,text="Add Water",width = 12, command=self.clickaddwater) # Button for adding consumed water
        self.buttonaddwater.grid(row = 6,column=1,sticky="W") 


        self.labelresult = tk.Label(self.root,text="Show the statistics? ")
        self.labelresult.grid(row=8,column=0,sticky='W')
        self.buttonshowstat = tk.Button(self.root,text="Show",width = 12, command=self.clickshowstat) # button for showing statistics
        self.buttonshowstat.grid(row = 8,column=1,sticky="W") 



        self.update_clock()
        self.root.mainloop()

    # Event handler for button- change settings
    def clicksettings(self):
        
        entered_newg =  self.varglass.get()
        entered_newt =  self.vartotal.get()
        entered_newn =  self.varnotiinterval.get()

        self.settings.set_glass(entered_newg)
        self.settings.set_totalQ(entered_newt)
        self.settings.set_notify_interval(entered_newn)

        labelchangesettings = tk.Label(self.root,text="New Settings-   Water glass:"+self.settings.get_glass()+" Total Quantity:"+self.settings.get_totalQ()+" Noto Interval:"+self.settings.get_notify_interval())
        labelchangesettings.grid(row=5,column=0,sticky='W')
        print("Settings Changed: glass-",self.settings.get_glass())


    # Event handler for adding more consumed water
    def clickaddwater(self):
        updated_totaltoday = int(self.settings.get_glass()) + int(self.settings.get_totaltoday())
        self.settings.set_totaltoday(updated_totaltoday)
        
        self.texttotaltoday.delete(0.0,tk.END)
        self.addwater_text = "You have drunk "+str(self.settings.get_totaltoday())+"/"+str(self.settings.get_totalQ())+" today."
        self.texttotaltoday.insert(tk.END,self.addwater_text) # Show the total consumed water today
        print("Now total drunk today: ",self.settings.get_totaltoday())

    # Event handler for showing stats
    def clickshowstat(self):
        aggregation = Aggregation()
        aggregation.showstat()
        

    """
        This is the most important logical part of this project
        Input: none
        Output:
            (i) Reset the amount to 0 if it it 00:00:00
            (ii) Log the consumed water for the previous day
            (iii) Generate the warning if consumed less wate than needed
            (iv) Send timely notification
    """
    def update_clock(self):
        date = time.strftime("%d-%b-%Y")
        now = time.strftime("%H:%M:%S")
        now = now.split(':')
        hour = int(now[0])
        minute= int(now[1])
        second = int(now[2])
        print("Hour: ",hour)

                                                                    # Reset the amount today and log the amount
        if hour==0 and minute==0 and second==0:
            log = str(self.settings.get_totaltoday())+","+date
            with open("log.csv", "a") as myfile:
                myfile.write(log)
            self.settings.set_totaltoday(0)
            


                                                                    # Generate the warning
        Noti_message = "Please Drink Water. Your consumption today: "+str(self.settings.get_totaltoday())+"/"+str(self.settings.get_totalQ())
        if hour>17 and self.settings.get_totaltoday<(self.settings.get_totalQ()/2):
            Noti_message= "Warning!! Warning!! You Drunk too little water today"

                                                                    # Send timely notification
        noti_interval= self.settings.get_notify_interval()
        if noti_interval=="10":
            if second%10==0:
                self.notifications.send_notification(Noti_message)
        elif noti_interval=="1800":
            if minute%30==0:
                self.notifications.send_notification(Noti_message)
        elif noti_interval=="3600":
            if minute%60==0 and second%60==0:
                self.notifications.send_notification(Noti_message)
        elif noti_interval=="7200":
            if minute%60==0 and second%60==0 and hour%2==0:
                self.notifications.send_notification(Noti_message)
            
        
        self.root.after(1000, self.update_clock)



def main():
    print("Starting The App")

    # Prepare the objects for the driver class
    window = tk.Tk()
    notifications = Notification()
    settings = Settings()

    # Call the driver class
    app=App(window,notifications,settings)



if __name__ == "__main__":
    main()
