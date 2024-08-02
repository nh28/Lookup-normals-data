import os
import tkinter as tk
from tkinter import BooleanVar, Button, Listbox, ttk
from DataFrameTable import DataFrameTable

class StationDataScreen():
    def __init__(self, station_name, df, all_elements, all_months, all_station_data):
        self.station_name = station_name
        self.df = df
        self.all_elements = all_elements
        self.all_months = all_months
        self.all_station_data = all_station_data
        self.show_station_data()
    
    def show_station_data(self):
        """
        Creates the station data screen which will be able to contain all the elements for the user to see.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        self.station_data_screen = tk.Toplevel()
        self.station_data_screen.title("Station Data Screen")

        self.station_data_screen.grid_columnconfigure(0, weight=1)
        self.station_data_screen.grid_columnconfigure(1, weight=3)
        self.station_data_screen.grid_rowconfigure(0, weight=3)
        self.station_data_screen.grid_rowconfigure(1, weight=1)
        
        self.create_widgets_frame()
        self.create_download_frame()
        self.create_tree_frame()

    def create_widgets_frame(self):
        """
        Creates the widgets frame that allows the user to select stations or elements they would like to view.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        widgets_frame = ttk.LabelFrame(self.station_data_screen)
        widgets_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        widgets_frame.grid_columnconfigure(0, weight=1)
        widgets_frame.grid_columnconfigure(1, weight=3)
        widgets_frame.grid_columnconfigure(2, weight=0)
        
        widgets_frame.grid_rowconfigure(0, weight=0)
        widgets_frame.grid_rowconfigure(1, weight=1)
        widgets_frame.grid_rowconfigure(2, weight=0)
        widgets_frame.grid_rowconfigure(3, weight=0)

        header1 = ttk.Label(widgets_frame, text="Months")
        header1.grid(row=0, column=0, sticky='nsew')

        header2 = ttk.Label(widgets_frame, text="Normals Elements")
        header2.grid(row=0, column=1, sticky='nsew')

        self.month_entry = Listbox(widgets_frame, height=13, width=10, selectmode="multiple", exportselection=0)
        self.month_entry.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        for value in self.all_months:
            self.month_entry.insert(tk.END, value)

        self.b = BooleanVar()
        all_mo = ttk.Checkbutton(widgets_frame, text="All Months", variable=self.b, command=self.select_all_mo)
        all_mo.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.element_entry = Listbox(widgets_frame, height=25, width=55, selectmode="multiple", exportselection=0)
        self.element_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        for value in self.all_elements:
            self.element_entry.insert(tk.END, value)

        self.a = BooleanVar()
        all_el = ttk.Checkbutton(widgets_frame, text="All Elements", variable=self.a, command=self.select_all_el)
        all_el.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(widgets_frame, orient="vertical", command=self.on_vertical_scroll)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.element_entry.config(yscrollcommand=scrollbar.set)

        update_button = Button(widgets_frame, text='Update', command=self.update)
        update_button.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

    def create_download_frame(self):
        """
        Creates the download frame that allows the user to download the xlsx or csv file of the data.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """  
        download_frame = ttk.LabelFrame(self.station_data_screen, text="Download")
        download_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        download_frame.grid_columnconfigure(0, weight=1)
        download_frame.grid_columnconfigure(1, weight=1)
        download_frame.grid_rowconfigure(0, weight=1)
        download_frame.grid_rowconfigure(1, weight=1)
        
        self.c = BooleanVar()
        self.d = BooleanVar()
        excel = ttk.Checkbutton(download_frame, text="XLSX", variable=self.c)
        excel.grid(row=0, column=0, padx=5, pady=10, sticky='w')
        
        csv = ttk.Checkbutton(download_frame, text="CSV", variable=self.d)
        csv.grid(row=0, column=1, padx=5, pady=10, sticky='w')
        
        download_button = Button(download_frame, text='Download', command=self.download)
        download_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def create_tree_frame(self):
        """
        Creates the tree frame with a table that displays all the data.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        tree_frame = ttk.LabelFrame(self.station_data_screen, text="Station Data")
        tree_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(1, weight=1)
        tree_frame.grid_columnconfigure(2, weight=0)
        tree_frame.grid_rowconfigure(0, weight=0)
        tree_frame.grid_rowconfigure(1, weight=1)
        tree_frame.grid_rowconfigure(2, weight=0)
        tree_frame.grid_rowconfigure(3, weight=0) 

        header1 = ttk.Label(tree_frame, text="Metadata")
        header1.grid(row=0, column=0, sticky='nsew')

        header2 = ttk.Label(tree_frame, text="Normals Data")
        header2.grid(row=0, column=1, sticky='ns')
        
        self.frame = DataFrameTable(tree_frame, dataframe=self.df)
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.frame.tree.yview)
        tree_scroll.grid(row=1, column=2, sticky='ns')
        self.frame.tree.config(yscrollcommand=tree_scroll.set)

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.frame.tree.xview)
        tree_scroll_x.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.frame.tree.config(xscrollcommand=tree_scroll_x.set)

        reset_spacing = ttk.Button(tree_frame, text="Reset Spacing", command=self.frame.reset_spacing)
        reset_spacing.grid(row=3, column=0, sticky='ns')
        reset_filter = ttk.Button(tree_frame, text="Reset Filters", command=self.frame.reset_filters)
        reset_filter.grid(row=3, column=1, sticky='ns')

    def on_vertical_scroll(self, *args):
        """
        Manages the element listbox's scroll feature.

        Parameters:
        self: The instance of the TkinterGUI.
        *args: Allows a function to accept any number of positional arguments.

        Returns:
        None
        """
        self.element_entry.yview(*args)

    def download(self):
        """
        Downloads either xlsx, csv, or both to the users Downloads folder on their device.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        name = "Normals_Data_Comparison_"
        station = self.station_name.replace(" ", "_")
        if self.c.get():
            name = name + station + ".xlsx"
            excel_file_path = os.path.join(downloads_folder, name)
            self.df.to_excel(excel_file_path, index=False)
        if self.d.get():
            name = name + station + ".csv"
            csv_file_path = os.path.join(downloads_folder, name)
            self.df.to_csv(csv_file_path, index=False)

    def update(self):
        """
        Updates the table based on the elements and months the user selected.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        selected_elements = self.element_entry.curselection()
        highlighted_elements = [self.element_entry.get(index) for index in selected_elements]
        
        selected_months = self.month_entry.curselection()
        highlighted_months = [self.month_entry.get(index) for index in selected_months]
        
        filtered_df = self.df[self.df['ELEMENT NAME'].isin(highlighted_elements)]
        filtered_df = filtered_df[filtered_df['Month'].isin(highlighted_months)]
        self.frame.update_dataframe(filtered_df)

    def select_all_el(self):
        """
        Highlights all the elements when the user presses All Elements button.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        if self.a.get():
            self.element_entry.selection_set(0, 'end')
        else:
            self.element_entry.selection_clear(0, 'end')

    def select_all_mo(self):
        """
        Highlights all the months when the user presses All Months button.

        Parameters:
        self: The instance of the TkinterGUI.

        Returns:
        None
        """
        if self.b.get():
            self.month_entry.selection_set(0, 'end')
        else:
            self.month_entry.selection_clear(0, 'end')