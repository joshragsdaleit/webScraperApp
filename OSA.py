import tkinter
import tkinter.messagebox
import customtkinter
from bs4 import BeautifulSoup
import requests
import webbrowser

# Tag options to select
switch_options = ['a', 'title', 'p', 'Full HTML', 'Get All Text', 'span', 'id']

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    

    # Main Constructor
    def __init__(self):
        super().__init__()

        # configure window
        self.title("OSA_V1.0.py")
        self.geometry(f"{1150}x{500}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1, 3), weight=0)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Overland Technical\nSolutions:\nWeb Scraper", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="About Overland", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Google Web Search", command=self.sidebar_button_event2)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Wikipedia Search", command=self.sidebar_button_event3)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark (Default)", "Light", "System"],
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
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Scraping Options")
        self.scrollable_frame.grid(row=0, rowspan=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = [] # Initializing array for Switch objects
        for i in range(len(switch_options)): # Creating Switches from the switch options, instating them into the grid
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=switch_options[i])
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)
            self.scrollable_frame_switches[i].select()
            if switch_options[i] != 'a' : # Disabling everything but the 'a' search option.
                self.scrollable_frame_switches[i].toggle()             

        # Donate to me please? Broke dad with four kids and relevant experience - I could really use a dev job too!
        self.donate = customtkinter.CTkButton(master=self, text="Donate to the Creator", command=self.donate_button_press, border_width=2)
        self.donate.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # set default value for Textbox
        self.textbox.insert(0.0, '''Welcome to my rudimentary web scraper!
You can use the output of these queries to build web scraping tools, or
to query specific websites for an actionable DOM tree.

Use the 'Google Web Search to the left to pre-fill a search URL for Google.
In the future, I plan to add the capability to build a custom input for querying
the DOM, to make it a one-size-fits-all tool. 
''')
        

    def change_appearance_mode_event(self, new_appearance_mode: str): # Function to update Appearance defaults that TKInter allows
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str): # Function to update Scaling
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self): # Clicking the 'about overland' button will take you to my website
        webbrowser.open('http://www.overlandtechnicalsolutions.com', new=2)

    def sidebar_button_event2(self): # fill Entry box with Google Search default URL 
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, "https://www.google.com/search?q=")

    def sidebar_button_event3(self): # fill Entry box with Google Search default URL 
        self.entry.delete(0, tkinter.END)
        self.entry.insert(0, "https://en.wikipedia.org/wiki/")        

    def donate_button_press(self): # Open CashApp for donations
        webbrowser.open('https://cash.app/$Jrags2010', new=2)

    def scrape_button_press(self):
        # Clear the textbox
        self.textbox.delete("0.0", tkinter.END)
        #  Perform Request for data based on input from self.entry
        url = self.entry.get()
        try:
            response = requests.get(url, timeout=5) 
        except Exception as err:
            self.textbox.insert(tkinter.END, "" + str(err) + " - Did you supply a URL?\n")

        content = BeautifulSoup(response.content, "html.parser") #  Gathering Page Content
        i = 0 # Initializing variable for for loop
        for item in range(len(switch_options)): # for all items inside switch_options
            self.textbox.insert(tkinter.END, "\nSearching response for " + switch_options[i] + " tags. \n" + switch_options[i] + " found: \n")
            if self.scrollable_frame_switches[i].get() == True: # if the switch is enabled
                try:
                    if switch_options[i] == 'a':    # and the tag to search is 'a'
                        for result in content.find_all('a'):  # result is now the a tags
                            final_result = result.get('href') # and final_result is now the href value
                            # if (".com" or ".net" or ".org") in final_result: 
                            self.textbox.insert(tkinter.END, "" + str(final_result) + "\n") # fill final_result to the textbox
                    elif switch_options[i] == 'Full HTML':  # If user wants the Full HTML structure
                        full_html = content.prettify() # Make it pretty
                        self.textbox.insert(tkinter.END, full_html) # Fill the textbox
                    elif switch_options[i] == 'Get All Text': # If they want all the text from the page, a la get_text()
                        all_text = content.get_text() # Then do so
                        self.textbox.insert(tkinter.END, all_text) # Once again, fill the textbox
                    else: # For switch options where the text matches the query, via bs4 documentation 
                        results = content.find_all(switch_options[i]) # Perform the query based on the switch text
                        for result in results:
                            final_result = result.get_text() # Pull the text from the results
                            self.textbox.insert(tkinter.END, final_result + "\n")  # Fill textbox with return data
                    i += 1 # Increment the variable
                except Exception as err:
                            self.textbox.insert(tkinter.END, "An exception occurred with a '" + switch_options[i] + "' tag. " + str(err) + "\n")
            else: # If a Switch is disabled
                self.textbox.insert(tkinter.END, "We didn't look for " + switch_options[i] + ' as the option is disabled.\n')
                i += 1
        


# BS4 Documentation for reference - https://www.crummy.com/software/BeautifulSoup/bs4/doc/

# Call Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()
