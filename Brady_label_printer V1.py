
from tkinter import Tk, W, E, filedialog, StringVar, LabelFrame, Listbox, Menu
from tkinter.ttk import Frame, Button, Entry, Style, Label
from lib.BPL_utils import *
from shutil import copyfile
import os, stat, ntpath, time



class Example(Frame):

    def __init__(self): 
        super().__init__() 
        self.initUI()
 
    def initUI(self):
        self.home_dir = os.getcwd()
        self.master.title("Brady Label Printer")

        # Menu Bar
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # File Menu
        file = Menu(menu, tearoff=0)
        file.add_command(label="Open...", command=self.open_cable_csv)

        # Printer Menu
        printer_menu = Menu(menu, tearoff=0)
        printer_menu.add_command(label="List printers", command=self.list_printers)
        
        # add File Menu to Menu Bar
        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Printer", menu=printer_menu)

        # Style and padding
        Style().configure("TButton", padding=(3, 5, 3, 5), font='serif 10')
        self.columnconfigure(0, pad=3) 
        self.rowconfigure(0, pad=3)

        # Full path to cable CSV file
        self.cable_csv_path = StringVar()
        self.cable_csv_path.set("No CSV file selected")
        # Cable assy dwg number
        self.cable_assy_num = StringVar()
        self.cable_assy_num.set("No cable labels")

        # Configure the main widget group
        grp_main = LabelFrame(self.master, text="PDAL")
        grp_main.grid(row=0, column=0)
        grp_main.config(padx=50, pady=20)

        # Configure the cable labels widget group
        grp_cbllbl = LabelFrame(self.master, text="Cable Labels")
        grp_cbllbl.grid(row=1, column=0)
        grp_cbllbl.config(padx=50, pady=20)
        
        # Cable label file path
        cable_label_file = Label(grp_cbllbl, textvariable = self.cable_csv_path, width=40)
        cable_label_file.grid(row=0, column=0)
        btn_open_cable_csv = Button(grp_cbllbl, text="Open cable label CSV", command=self.open_cable_csv)
        btn_open_cable_csv.grid(row=1, column=0)

        # Cable Label Listbox
        lstbx_cables_lbl = Label(grp_cbllbl, textvariable = self.cable_assy_num)
        lstbx_cables_lbl.grid(row=0, column=1)
        self.lstbx_cables = Listbox(grp_cbllbl, selectmode="extended", width=80)
        self.lstbx_cables.grid(row=1, column=1)
        
        btn_print_labels = Button(grp_cbllbl, text="Print labels", command=self.print_labels)
        btn_print_labels.grid(row=2, column=1)

        btn_quit = Button(self.master, text="Quit", command=self.quit)
        btn_quit.grid(row=3, column=0)

    def open_cable_csv(self):
        filepath = filedialog.askopenfilename()
        self.cable_csv_path.set(filepath)
        fp_sp = ntpath.split(filepath)
        filename = fp_sp[1]
        fn_sp = filename.split(".")
        self.cable_assy_num.set(fn_sp[0])
        self.lstbx_cables.delete(0, "end")
        f_csv = open(filepath, "r")
        for line in f_csv:
            self.lstbx_cables.insert("end", line)

    def list_printers(self):
        BPL_EnumPrinters()

    def print_labels(self):
        cbllbl_dir = self.cable_assy_num.get()
        cbllbl_dir = self.home_dir + '\\print\\' + cbllbl_dir
        if(not os.path.isdir(cbllbl_dir)):
            os.mkdir(cbllbl_dir)
        filepath = self.cable_csv_path.get()
        GenerateXMLinFives(cbllbl_dir, filepath)
        lbl_files = os.listdir(cbllbl_dir)
        for f in lbl_files:
            SendToBP33(cbllbl_dir + "\\" + f, False)
            time.sleep(2)
            #self.lstbx_cables.insert("end", "Sent " + f + " to printer")
            print("Sent " + f + " to printer")
        #self.lstbx_cables.insert("end", "Finished!")
        print("Finished!")

    def quit(self):
        self.master.destroy()

def main():
    app = Example()
    app.mainloop()

main()
