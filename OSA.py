import tkinter
import tkinter.messagebox
import customtkinter
from bs4 import BeautifulSoup
import requests
import webbrowser

# Tag options to select
switch_options = ['a', 'title', 'p', 'Full HTML', 'Get All Text']

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    

    # Main Constructor
    def __init__(self):
        super().__init__()

        # configure window
        self.title("scrapeApp1.0.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1, 3), weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Overland Technical Solutions", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="URL Scraper", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Google Web Search", command=self.sidebar_button_event2)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        #  self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        #  self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["100%", "80%", "90%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Input URL Here")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(master=self, text="Scrape URL", command=self.scrape_button_press, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=650)
        self.textbox.grid(row=0, rowspan=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Scrape Options")
        self.scrollable_frame.grid(row=0, rowspan=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = [] # Initializing array for Switch objects
        for i in range(len(switch_options)): # Creating Switches from the switch options
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=switch_options[i])
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)
            self.scrollable_frame_switches[i].select()
            if switch_options[i] != 'a' : # Disabling everything but the 'a' search option.
                self.scrollable_frame_switches[i].toggle()             

        # Donate to me please?
        self.donate = customtkinter.CTkButton(master=self, text="Donate to the Creator!", command=self.donate_button_press, border_width=2)
        self.donate.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # set default value for Textbox
        self.textbox.insert(0.0, "Welcome to my rudimentary web scraper! I plan to use this to create web scraping apps, and we'll see where it goes from here!\n\n")
        

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        webbrowser.open('http://www.overlandtechnicalsolutions.com', new=2)

    def sidebar_button_event2(self):
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, "https://www.google.com/search?q=")

    def donate_button_press(self):
        webbrowser.open('https://cash.app/$Jrags2010', new=2)

    def scrape_button_press(self):
        # Clear the textbox
        self.textbox.delete("0.0", tkinter.END)
        #  Performing Request for data
        url = self.entry.get()
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser") #  Gathering Page Content
        i = 0
        for item in range(len(switch_options)): # for all items inside switch_options
            self.textbox.insert(tkinter.END, "\nSearching response for " + switch_options[i] + " tags. \n" + switch_options[i] + " found: \n")
            if self.scrollable_frame_switches[i].get() == True: # if the switch is enabled
                try:
                    if switch_options[i] == 'a':    # and the tag to search is 'a'
                        for result in content.find_all('a'):  # result is now the a tags
                            final_result = result.get('href') # and final_result is now the href value
                            # if (".com" or ".net" or ".org") in final_result: 
                            self.textbox.insert(tkinter.END, "" + str(final_result) + "\n")
                    elif switch_options[i] == 'Full HTML': 
                        full_html = content.prettify()
                        self.textbox.insert(tkinter.END, full_html)
                    elif switch_options[i] == 'Get All Text':
                        all_text = content.get_text()
                        self.textbox.insert(tkinter.END, all_text)
                    else:
                        results = content.find_all(switch_options[i])
                        for result in results:
                            final_result = result.get_text()
                            self.textbox.insert(tkinter.END, final_result + "\n") 
                    i += 1
                except Exception as err:
                            self.textbox.insert(tkinter.END, "An exception occurred with a '" + switch_options[i] + "' tag. " + str(err) + "\n")
            else:
                self.textbox.insert(tkinter.END, "We didn't look for " + switch_options[i] + ' as the option is disabled.\n')
                i += 1
        
        '''
        for item in self.scrollable_frame_switches:
            switches_text = self.scrollable_frame_switches[i]
            if switches_text.get() == True:
                result = content.find_all(switches_text)
                
            i += 1
        '''
'''

        self.scrollable_frame_switches = []
        for i in range(len(switch_options)):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"{switch_options[i]}")

As the error message indicates, the tk module does not have a function named get. 
It might have plenty of classes whose instances have a get method, but you can't access them the way you're doing.

If you're trying to get the contents of the Entry, you should assign it to a name, and call get on that instead:

def EP(): # Enter inputs from values typed in
      xf_In = e_xf.get(e_xf)
      print(xf_In)
Note that this assignment is different from doing e_xf = tk.Entry(root).grid(row=0, column=1). 
If you do that, then e_xf will be bound to the return value of grid, rather than the Entry instance. 
Grid returns None, so trying to call get on that would only give you an AttributeError.

#...

e_xf = tk.Entry(root)
e_xf.grid(row=0, column=1)

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

'''


if __name__ == "__main__":
    app = App()
    app.mainloop()
