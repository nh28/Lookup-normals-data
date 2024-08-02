import time
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from tqdm import tqdm
from ARKEON import ARKEON
from Table import Table

login=False
arkeon = ARKEON()

def login_command():
    """
    Checks the credentials of the user to log them into the ARKEON database.

    Parameters:
    None

    Returns:
    None
    """
    global login
    username = username_entry.get()
    password = password_entry.get()

    if login:
        status_label.config(text="Already Logged In")
    else:
        if arkeon.connect(username, password):
            login=True
            status_label.config(text="Successfully Logged In")
        else:
            messagebox.showerror("Error", "Failed to connect to ARKEON. Please check your username and password.")

def update_data():
    """
    Gathers and formats all of the data from ARKEON.

    Parameters:
    None
    
    Returns:
    None
    """
    global login
    if login:
        status_label.config(text="Gathering Data from ARKEON")
        root.update_idletasks()
        
        
        try:
            dataframes = [
                ('df_71', ['STN_ID', 'NORMAL_ID', 'MONTH', 'VALUE', 'FIRST_OCCURRENCE_DATE', 'NORMAL_CODE'], 'NORMALS.NORMALS_DATA'),
                ('df_81', ['STN_ID', 'NORMAL_ID', 'MONTH', 'VALUE', 'FIRST_OCCURRENCE_DATE', 'NORMAL_CODE'], 'NORMALS_1981.NORMALS_DATA'),
                ('df_91', ['STN_ID', 'NORMAL_ID', 'MONTH', 'VALUE', 'FIRST_OCCURRENCE_DATE', 'NORMAL_CODE'], 'NORMALS_1991.NORMALS_DATA')
            ]

            data = {}
            for name, columns, table in tqdm(dataframes, desc="Fetching Data from ARKEON"):
                data[name] = arkeon.get_dataframe(columns, table, [], False)

            df_71 = data['df_71']
            df_81 = data['df_81']
            df_91 = data['df_91']
            
        except Exception as e:
            messagebox.showerror("Error", f"Error while gathering data: {str(e)}")
            return
        
        status_label.config(text="Finished gathering data from ARKEON. Formatting...")
        root.update_idletasks()
        
        all_stations = arkeon.get_all_stations()
        all_elements = arkeon.get_all_elements()
        all_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

        table = Table(arkeon, all_elements, all_months)
        
        all_stations_data = []
        
        for station in tqdm(all_stations, desc="Formatting all Stations"):
            indv_station = table.get_all_data(station, df_71, df_81, df_91)
            all_stations_data.extend(indv_station)
        
        headers = ['STN ID', 'STN/LOC NAME', 'CLIMATE ID', 'PROV', 'NORMAL ID', 'ELEMENT NAME', 'Month', 'Value (71)', 'Code (71)', 'Date (71)', 'Value (81)', 'Code (81)', 'Date (81)', 'Value (91)', 'Code (91)', 'Date (91)']
        df = pd.DataFrame(all_stations_data, columns=headers)
        df.to_csv('Input_Files/stations_data_new.csv', index=False)
        status_label.config(text="Data has been saved to stations_data_new.csv")
        
        status_label.config(text="Done")
    else:
        messagebox.showerror("Error", "Please login.")


root = tk.Tk()
root.title("Stations Data Updater")
root.geometry("400x200")

tk.Label(root, text="Username:").pack(pady=10)
username_entry = tk.Entry(root)
username_entry
username_entry.pack()

tk.Label(root, text="Password:").pack(pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

login_button = tk.Button(root, text="Login", command=login_command)
login_button.pack()

update_button = tk.Button(root, text="Update Data", command=update_data)
update_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
