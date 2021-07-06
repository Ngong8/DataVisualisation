import tkinter as tk
import tkinter.ttk as ttk
from tkinter_custom_button import TkinterCustomButton
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from configparser import ConfigParser
import os.path
# For creating a new configuration file if it doesn't exists
configObj = ConfigParser()
configObj["Themes"] = {
    "isDark": "False",
    "lblColor": "#005e78","bgColor": "#e0e0e0",
    "figtxtColor": "black","legColor": "white",
    
    "lblColorLight": "#005e78","bgColorLight": "#e0e0e0",
    "figtxtColorLight": "black","legColorLight": "white",
    "lblColorDark": "#00c8ff","bgColorDark": "#2e2e2e",
    "figtxtColorDark": "white","legColorDark": "black"
}
if not os.path.isfile('config.ini'):
    with open('config.ini', 'w') as conf:
        configObj.write(conf)
# JUST READ IT WHEN IT'S CREATED OR STILL EXISTED
configObj.read("config.ini")
themeSection = configObj["Themes"]
lblColor = themeSection["lblColor"]; bgColor = themeSection["bgColor"]
figtxtColor = themeSection["figtxtColor"]; legColor = themeSection["legColor"]
# Initialise the program and sets its background color
root = tk.Tk()
root['bg'] = bgColor
nearFuture = 'Glitch Slap' # Custom font for the texts used in the program

class Main(tk.Frame): # This class should used for main menu, but this is unused for now...
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.nearFuture = 'Glitch Slap'
        pd.set_option('display.max_rows', None)
        url = "https://raw.githubusercontent.com/ynshung/covid-19-malaysia/master/covid-19-my-states-cases.csv"
        self.retrieveData = pd.read_csv(url, names=["Date","Perlis","Kedah","Penang","Perak","Selangor",
                                            "Negeri Sembilan","Melaka","Johor","Pahang","Terengganu",
                                            "Kelantan","Sabah","Sarawak","Kuala Lumpur","Putrajaya","Labuan"],
                                header=0, parse_dates=['Date'], dayfirst=True, na_values=['-'])
        self.retrieveData.fillna(0,inplace=True)
        self.initUI()
    
    def initUI(self): # Initialize tons of buttons and a figure to display different graphs
        # Pre-define some values for users to choose the range of date and particular area
        self.optionsDate = tk.StringVar(); self.optionsState = tk.StringVar()
        self.valuesDate = ['2020-03-13 2020-03-31','2020-04-01 2020-04-30','2020-05-01 2020-05-31',
                           '2020-06-01 2020-06-30','2020-07-01 2020-07-31','2020-08-01 2020-08-31',
                           '2020-09-01 2020-09-30','2020-10-01 2020-10-31','2020-11-01 2020-11-30',
                           '2020-12-01 2020-12-31']
        self.valuesState = ['Perlis','Kedah','Penang','Perak','Selangor','Negeri Sembilan','Melaka',
                            'Johor','Pahang','Terengganu','Kelantan','Sabah','Sarawak','Kuala Lumpur',
                            'Putrajaya','Labuan']
        # Create labels to guide users to use drop down boxes
        self.lblDate = tk.Label(root, text="Choose the destined month range: ", font=(self.nearFuture, 12), 
                                fg='#00c8ff', bg='#2e2e2e')
        self.lblState = tk.Label(root, text="Choose the particular state/federal territory: ", 
                                 font=(self.nearFuture, 12), fg='#00c8ff', bg='#2e2e2e')
        # Create a drop down box for users to select the specific range of months
        self.oDate = ttk.Combobox(root, width=20, textvariable=self.optionsDate, font=(self.nearFuture, 12))
        self.oDate['values'] = self.valuesDate
        self.oDate['state'] = 'readonly'; self.oDate.current(0)
        # Create another drop down box for users to choose the said state/federal territory
        self.oState = ttk.Combobox(root, width=20, textvariable=self.optionsState, font=(self.nearFuture, 12))
        self.oState['values'] = self.valuesState
        self.oState['state'] = 'readonly'; self.oState.current(0)
        # Create figure
        self.fig = Figure(figsize=(20,4), dpi=150, tight_layout = True); self.a = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('#2e2e2e'); self.a.set_facecolor('#2e2e2e')
        # Create modern look buttons and have their own working attached
        self.BtnTheme = TkinterCustomButton(bg_color=None, fg_color="#0092c7", hover_color="#57c0e6", 
                                           text_font=(self.nearFuture, 12), text="Change theme",
                                           text_color="white", corner_radius=20, width=160, height=32, 
                                           hover=True, command=self.update_bar, cursor="hand2")
        self.BtnApply = TkinterCustomButton(bg_color=None, fg_color="#0092c7", hover_color="#57c0e6", 
                                           text_font=(self.nearFuture, 12), text="Apply",text_color="white", 
                                           corner_radius=20, width=100, height=32, hover=True, 
                                           command=self.update_bar, cursor="hand2")
        self.BtnQuit = TkinterCustomButton(bg_color=None, fg_color="#c70000", hover_color="#ff6b6b", 
                                           text_font=(self.nearFuture, 12), text="Quit",text_color="black", 
                                           corner_radius=20, width=100, height=32, hover=True, 
                                           command=self.quit, cursor="hand2")
        # Arrange these widgets' positions
        self.lblDate.place(x=10, y=10)
        self.oDate.place(x=10, y=40)
        self.lblState.place(x=300, y=10)
        self.oState.place(x=300, y=40)
        self.BtnTheme.place(x=700, y=10)
        self.BtnApply.place(x=240, y=100) 
        self.BtnQuit.place(x=20, y=100)
        # Finalizing the application of the graph integrated with the TK GUI
        self.canvas_agg = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_agg.get_tk_widget().pack()
        self.pack(side=tk.BOTTOM)
        # Call to show the figure upon run the program, can be called again after clicked "Apply" button
        self.update_bar()
    
    def update_bar(self):
        self.a.clear() # The previous data will be cleared first...
        # ...Then, apply the new data for the figure after clicked "Apply" button
        getDate = self.oDate.get(); getState = self.oState.get()
        self.minDate,self.maxDate = getDate.split(' ')
        self.stateName = getState
        # Take a specific range of date of a state/federal territory, then apply to a new var for calling
        mask = (self.retrieveData['Date'] >= self.minDate) & (self.retrieveData['Date'] <= self.maxDate)
        retrieve_data = self.retrieveData.loc[mask]
        maskedDate = retrieve_data['Date']
        # How should the charts display to the people eyes
        b = self.a.bar(maskedDate, retrieve_data[self.stateName], label=self.stateName+" total cases")
        self.a.set_xlabel('Date', fontweight='bold', color='white')
        self.a.set_ylabel('Accumulated case(s)', fontweight='bold', color='white')
        self.a.set_xticks(maskedDate[::2])
        self.a.tick_params(axis='x', labelrotation=0, labelsize=5, colors='white')
        self.a.tick_params(axis='y', labelrotation=0, labelsize=6, colors='white')
        self.a.bar_label(b, label_type='center', fontsize=5, fontweight='bold', color='white')
        self.a.set_title('Total cases of COVID-19 cases by date', color='white', fontweight='bold')
        self.a.legend(facecolor='black', edgecolor='white', labelcolor='white', loc='upper left', 
                      framealpha=0.4, prop={'weight':'bold','size':6}) 
        self.a.grid(True)
        # Draw the figure to show visualised data
        self.fig.canvas.draw()

class DailyCasePage(tk.Frame): # This class is used for the page which showing cases daily in a said month

    def __init__(self, master=None): # Initialise the scene and input data from a csv file
        tk.Frame.__init__(self, master)
        pd.set_option('display.max_rows', None)
        url = "https://raw.githubusercontent.com/ynshung/covid-19-malaysia/master/covid-19-my-states-cases.csv"
        self.retrieveData = pd.read_csv(url, names=["Date","Perlis","Kedah","Penang","Perak","Selangor",
                                            "Negeri Sembilan","Melaka","Johor","Pahang","Terengganu",
                                            "Kelantan","Sabah","Sarawak","Kuala Lumpur","Putrajaya","Labuan"],
                                header=0, parse_dates=['Date'], dayfirst=True, na_values=['-'])
        self.retrieveData.fillna(0,inplace=True)
        self.initValues()
    
    def initValues(self): # Pre-define some values for the range of date and particular area
        self.optionsDate = tk.StringVar(); self.optionsState = tk.StringVar()
        self.valuesDate = ['2020-03-13 2020-03-31','2020-04-01 2020-04-30','2020-05-01 2020-05-31',
                           '2020-06-01 2020-06-30','2020-07-01 2020-07-31','2020-08-01 2020-08-31',
                           '2020-09-01 2020-09-30','2020-10-01 2020-10-31','2020-11-01 2020-11-30',
                           '2020-12-01 2020-12-31',
                           '2021-01-01 2021-01-31','2021-02-01 2021-02-28','2021-03-01 2021-03-31',
                           '2021-04-01 2021-04-30','2021-05-01 2021-05-31','2021-06-01 2021-06-30',
                           '2021-07-01 2021-07-31','2021-08-01 2021-08-31','2021-09-01 2021-09-30',
                           '2021-10-01 2021-10-31','2021-11-01 2021-11-30','2021-12-01 2021-12-31']
        self.valuesState = ['Perlis','Kedah','Penang','Perak','Selangor','Negeri Sembilan','Melaka',
                            'Johor','Pahang','Terengganu','Kelantan','Sabah','Sarawak','Kuala Lumpur',
                            'Putrajaya','Labuan']
        self.initUI()
    
    def initUI(self): # Initialize tons of buttons and a figure to display different graphs
        matplotlib.rcParams['font.family'] = nearFuture # Set ALL graph's font family to this...
        # Create labels to guide users to use drop down boxes
        self.lblDate = tk.Label(root, text="Choose the destined month range:", font=(nearFuture, 12), 
                                fg=lblColor, bg=bgColor)
        self.lblState = tk.Label(root, text="Choose the particular state/federal territory:", 
                                 font=(nearFuture, 12), fg=lblColor, bg=bgColor)
        # Create a drop down box for users to select the specific range of months
        self.oDate = ttk.Combobox(root, width=20, textvariable=self.optionsDate, font=(nearFuture, 12))
        self.oDate['values'] = self.valuesDate
        self.oDate['state'] = 'readonly'; self.oDate.current(0)
        # Create another drop down box for users to choose the said state/federal territory
        self.oState = ttk.Combobox(root, width=20, textvariable=self.optionsState, font=(nearFuture, 12))
        self.oState['values'] = self.valuesState
        self.oState['state'] = 'readonly'; self.oState.current(0)
        # Create figure and set its background colour
        self.fig = Figure(figsize=(20,4), dpi=150, tight_layout = True)
        self.a = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor(bgColor)
        self.a.set_facecolor(bgColor)
        # For creating a bar chart later when calling update_bar()
        self.b = None
        # Create modern look buttons and have their own working attached
        self.BtnTheme = TkinterCustomButton(bg_color=None, fg_color="#0092c7", hover_color="#57c0e6", 
                                           text_font=(nearFuture, 12), text="Change theme",
                                           text_color="white", corner_radius=10, width=160, height=32, 
                                           hover=True, command=self.toggleTheme, cursor="hand2")
        self.BtnApply = TkinterCustomButton(bg_color=None, fg_color="#0092c7", hover_color="#57c0e6", 
                                           text_font=(nearFuture, 12), text="Apply",text_color="white", 
                                           corner_radius=10, width=100, height=32, hover=True, 
                                           command=self.update_bar, cursor="hand2")
        self.BtnQuit = TkinterCustomButton(bg_color=None, fg_color="#c70000", hover_color="#ff6b6b", 
                                           text_font=(nearFuture, 12), text="Quit",text_color="black", 
                                           corner_radius=10, width=100, height=32, hover=True, 
                                           command=self.quit, cursor="hand2")
        # Arrange these widgets' positions
        self.lblDate.place(x=10, y=10)
        self.oDate.place(x=10, y=40)
        self.lblState.place(x=300, y=10)
        self.oState.place(x=300, y=40)
        self.BtnTheme.place(x=700, y=30)
        self.BtnApply.place(x=240, y=100) 
        self.BtnQuit.place(x=20, y=100)
        # Finalizing the application of the graph integrated with the TK GUI
        self.canvas_agg = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_agg.get_tk_widget().pack()
        self.pack(side=tk.BOTTOM)
        # Call to show the figure upon run the program, can be called again after clicked "Apply" button
        self.update_bar()
    
    def update_bar(self):
        self.a.clear() # The previous data will be cleared first...
        # ...Then, apply the new data for the figure after clicked "Apply" button
        getDate = self.oDate.get(); getState = self.oState.get()
        self.minDate,self.maxDate = getDate.split(' ')
        self.stateName = getState
        # Take a specific range of date of a state/federal territory, then apply to a new var for calling
        mask = (self.retrieveData['Date'] >= self.minDate) & (self.retrieveData['Date'] <= self.maxDate)
        retrieve_data = self.retrieveData.loc[mask]
        maskedDate = retrieve_data['Date']
        # How should the charts display to the people eyes
        self.b = self.a.bar(maskedDate, retrieve_data[self.stateName], label=self.stateName+" total cases")
        self.a.set_xlabel('Date', fontweight='bold', color=figtxtColor)
        self.a.set_ylabel('Accumulated case(s)', fontweight='bold', color=figtxtColor)
        self.a.set_xticks(maskedDate[::2])
        self.a.tick_params(axis='x', labelrotation=0, labelsize=5, colors=figtxtColor)
        self.a.tick_params(axis='y', labelrotation=0, labelsize=6, colors=figtxtColor)
        self.a.bar_label(self.b, label_type='center', fontsize=5, fontweight='bold', color=figtxtColor)
        self.a.set_title('Total cases of COVID-19 cases by date', color=figtxtColor, fontweight='bold')
        self.a.legend(facecolor=legColor, edgecolor=figtxtColor, labelcolor=figtxtColor, loc='upper left', 
                      framealpha=0.4, prop={'weight':'bold','size':7}) 
        self.a.grid(True, color=figtxtColor, alpha=1); self.a.set_axisbelow(True)
        self.a.spines["top"].set_color(figtxtColor); self.a.spines["bottom"].set_color(figtxtColor)
        self.a.spines["left"].set_color(figtxtColor); self.a.spines["right"].set_color(figtxtColor)
        # Draw the figure to show visualised data
        self.fig.canvas.draw()
        
    def toggleTheme(self): # Toggle either you want light or dark theme!
        global lblColor; global bgColor
        global figtxtColor; global legColor
        if themeSection["isDark"] == "False": # Current is Light theme, going behind the SHADOW...
            themeSection["lblColor"] = themeSection["lblColorDark"]
            themeSection["bgColor"] = themeSection["bgColorDark"]
            themeSection["figtxtColor"] = themeSection["figtxtColorDark"]
            themeSection["legColor"] = themeSection["legColorDark"]
            themeSection["isDark"] = "True"
            with open('config.ini', 'w') as c: configObj.write(c)
        elif themeSection["isDark"] == "True": # Current is Dark theme, so let there be Light!
            themeSection["lblColor"] = themeSection["lblColorLight"]
            themeSection["bgColor"] = themeSection["bgColorLight"]
            themeSection["figtxtColor"] = themeSection["figtxtColorLight"]
            themeSection["legColor"] = themeSection["legColorLight"]
            themeSection["isDark"] = "False"
            with open('config.ini', 'w') as c: configObj.write(c)
        # Current colour settings changed for the variables below:
        lblColor = themeSection["lblColor"]; bgColor = themeSection["bgColor"]
        figtxtColor = themeSection["figtxtColor"]; legColor = themeSection["legColor"]
        print("Dark Theme: "+themeSection["isDark"])
        print(lblColor, bgColor, figtxtColor, legColor)
        # Just updating ALL of the colours of these buttons, figure, etc. to other colours
        root['bg'] = bgColor
        self.lblDate.config(fg=lblColor, bg=bgColor); self.lblState.config(fg=lblColor, bg=bgColor)
        self.BtnTheme.configure_color(bg_color=None)
        self.BtnApply.configure_color(bg_color=None) 
        self.BtnQuit.configure_color(bg_color=None)
        
        self.fig.patch.set_facecolor(bgColor); self.a.set_facecolor(bgColor)
        self.a.xaxis.label.set_color(figtxtColor); self.a.yaxis.label.set_color(figtxtColor)
        self.a.tick_params(axis='x', labelrotation=0, labelsize=5, colors=figtxtColor)
        self.a.tick_params(axis='y', labelrotation=0, labelsize=6, colors=figtxtColor)
        self.a.bar_label(self.b, label_type='center', fontsize=5, fontweight='bold', color=figtxtColor)
        self.a.set_title('Total cases of COVID-19 cases by date', color=figtxtColor, fontweight='bold')
        self.a.legend(facecolor=legColor, edgecolor=figtxtColor, labelcolor=figtxtColor, loc='upper left', 
                framealpha=0.4, prop={'weight':'bold','size':7}) 
        self.a.grid(True, color=figtxtColor, alpha=1); self.a.set_axisbelow(True)
        self.a.spines["top"].set_color(figtxtColor); self.a.spines["bottom"].set_color(figtxtColor)
        self.a.spines["left"].set_color(figtxtColor); self.a.spines["right"].set_color(figtxtColor)
        # And redraw the figure again as the theme has been changed
        self.fig.canvas.draw()

# The program's title and its resolution size
root.title("Data Visualization")
root.geometry("1280x720")
root.iconbitmap('DataVisualisation.ico')
# Run this particular page/scene upon the program started running
app = DailyCasePage(master=root)
app.mainloop()







