import logging
import tkinter as tk
from tkinter import messagebox
from ARKEON import ARKEON
import pandas as pd

from StationDataScreen import StationDataScreen

logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class TkinterGUI:
    def __init__(self, root):
        """
        Initialize a new instance of TkinterGUI.

        Parameters:
        self: The instance of the TkinterGUI.
        root: The initial frame created for the Login page.
        """
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x200")
        self.create_login_screen()

    def create_login_screen(self):
        """
        Sets up the Login screen with username and password entry's, as well as a Login button.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        """
        Validates the users credentials using ARKEON.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.arkeon = ARKEON()
        if self.arkeon.connect(username, password):
            self.load_data()
        else:
            logging.error("Login Failed", "Invalid username or password")
            messagebox.showerror("Login Failed", "Invalid username or password")

    def load_data(self):
        """
        Loads all the stations data from 1971, 1981, and 1991 (all in a csv file).

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        self.root.destroy()
        messagebox.showinfo(title=None, message='Data is loading...please press ok to start the loading process.')
        
        try:
           self.all_station_data = pd.read_csv("Input_Files/stations_data.csv")
        except Exception as e:
            logging.error("Error:" + str(e))
            messagebox.showerror(title='Error', message=str(e))
            return

        self.all_stations = self.arkeon.get_all_stations()
        self.all_elements = self.arkeon.get_all_elements()
        self.all_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

        self.create_station_screen()

    def create_station_screen(self):
        """
        Sets up the Station screen that allows the user to choose which station they would like to select.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        self.root = tk.Tk()
        self.root.title("Station Screen")

        tk.Label(self.root, text="Filter Stations:").pack(pady=10)
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind("<KeyRelease>", self.filter_stations)

        self.stations = tk.Listbox(self.root, width=50, height=10)
        self.stations.pack(padx=10, pady=5)

        for station in self.all_stations:
            self.stations.insert(tk.END, station)
        self.stations.selection_set(first=0)

        tk.Button(self.root, text="Go", command=self.on_select).pack(pady=10)
        self.root.mainloop()

    def filter_stations(self, event):
        """
        Filters the stations shown in the Listbox depending on what the user started to type in the entry box.

        Parameters:
        self: The instance of the TkinterGUI.
        event: The event object representing the key release event.

        Returns:
        None
        """
        keyword = self.entry.get().lower()
        self.stations.delete(0, tk.END)
        for station in self.all_stations:
            if station.lower().startswith(keyword.lower()):
                self.stations.insert(tk.END, station)

    def on_select(self):
        """
        Creates a dataframe of the chosen station's data.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        station = self.stations.get(tk.ACTIVE)
        self.user_station = station
        try:
            self.df = self.all_station_data[self.all_station_data['STN/LOC NAME'] == self.user_station]
            self.df = self.df.fillna("")
            
            StationDataScreen(station, self.df, self.all_elements, self.all_months, self.all_station_data)
        except Exception as e:
            logging.error("Error:" + str(e))
            messagebox.showerror(title='Error', message=str(e))
            

if __name__ == "__main__":
    """
    The main entry point for the Tkinter application.

    This block checks if the script is being run as the main program and
    not being imported as a module in another script. It initializes the
    Tkinter root window and the TkinterGUI application, then starts the
    Tkinter main event loop.

    Classes:
        TkinterGUI: The main class for the Tkinter application GUI.

    Functions:
        None

    Usage:
        Run this script directly to start the Tkinter application.
    """
    root = tk.Tk()
    app = TkinterGUI(root)
    root.mainloop()
