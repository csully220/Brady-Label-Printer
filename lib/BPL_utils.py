import win32print
import tkinter as tk
from tkinter import filedialog
import ntpath
import os
import math

xml_opening = '<?xml version="1.0"?>\n<bpl-document>\n'
#xml_defaults = '    <defaults>\n        <document units="inches" />\n        <printer tear-or-cut-between="after-job" />\n    </defaults>\n'
xml_defaults = '    <defaults>\n        <document units="inches" />\n        <printer tear-or-cut="none" />\n    </defaults>\n'
xml_labels = '    <labels>\n'
#xml_label = '        <label copies="1" width="2" height="3.75" offset-x="0.094" offset-y="-0.19" orientation="portrait" >\n' #offsets for OUR BP33
xml_label = '        <label copies="1" width="2" height="3.75" offset-x="0" offset-y="0" orientation="portrait" >\n' # no offsets - for loaner BP33
xml_label_wire = '        <label copies="1" width="2" height="0.45" offset-x="0" offset-y="0" orientation="portrait" >\n' # no offsets - for loaner BP33

def GenerateWireLabels(dir_name, filename):
    #print("Select the CSV file exported from AutoCAD containing label information...")
    
    fn_csv = filename
    
    num_lines = sum(1 for line in open(fn_csv))
    print(str(num_lines) + ' labels found for printing.')
    f_csv = open(fn_csv, "r")
    
    if ( num_lines % 5 ):
        num_files = math.floor(num_lines/5)+1
    else:
        num_files = num_lines/5
    
    print("num_files " + str(num_files))
    labels = f_csv.readlines()
    labels = [x.strip() for x in labels]
    
    for n in range(int(num_files)):
        lwrbnd = (n*5)
        uprbnd = (n*5)+5
        if ( uprbnd > len(labels) ):
            uprbnd = len(labels)
        lbls = labels[lwrbnd:uprbnd]
        #print(str(n) + ' ' + len(lbls))
        GenerateXMLfromListWire(lbls, dir_name + '\labels_' + str(n) + '.xml')


def GenerateXMLfromListWire(lbls, fn):
    if(len(lbls)):
        # Create a BPL file for writing to
        fn_bpl = fn

        f_bpl = open(fn_bpl, "w")

        # BPL Document opening tags
        f_bpl.write(xml_opening)
        f_bpl.write(xml_defaults)
        # Start labels
        f_bpl.write(xml_labels)

        n=0
        for lbl in lbls:

            # Start label
            if ( len(lbl.strip()) > 0 ):

                lines = lbl.split(',')

                # Write text tag for each of the three lines
                f_bpl.write('        <!-- LABEL ' + str(n + 1) + ' -->\n')
                n+=1
                f_bpl.write(xml_label_wire)

                txt_height = "0.25"
                for i in range(len(lines)):
                    line = lines[i].strip().strip("'")
                    if ( len(line) > 0):
                        f_bpl.write('            <!-- LINE ' + str(i + 1) + ' -->\n')
                        f_bpl.write('            <text position-x="0" position-y="0" align="center" bold="true" font-name="Courier New" >\n')
                        f_bpl.write('                <text-sizing>\n                    <manual height="' + txt_height + '" width="2" font-size="9" />\n                </text-sizing>\n')
                        f_bpl.write('                <datasource>\n                    <static-text value="' + line + '" />\n                </datasource>\n')
                        f_bpl.write('            </text>\n')
                # Close the label tag
                f_bpl.write('        </label>\n')

        # Close labels and document tags
        f_bpl.write('    </labels>\n')
        f_bpl.write('</bpl-document>')

        f_bpl.close()



def GenerateCableLabels(dir_name, filename):
    #print("Select the CSV file exported from AutoCAD containing label information...")
    
    fn_csv = filename
    
    num_lines = sum(1 for line in open(fn_csv))
    print(str(num_lines) + ' labels found for printing.')
    f_csv = open(fn_csv, "r")
    
    if ( num_lines % 5 ):
        num_files = math.floor(num_lines/5)+1
    else:
        num_files = num_lines/5
    
    print("num_files " + str(num_files))
    labels = f_csv.readlines()
    labels = [x.strip() for x in labels]
    
    for n in range(int(num_files)):
        lwrbnd = (n*5)
        uprbnd = (n*5)+5
        if ( uprbnd > len(labels) ):
            uprbnd = len(labels)
        lbls = labels[lwrbnd:uprbnd]
        #print(str(n) + ' ' + len(lbls))
        GenerateXMLfromList(lbls, dir_name + '\labels_' + str(n) + '.xml')


def GenerateXMLfromList(lbls, fn):
    if(len(lbls)):
        # Create a BPL file for writing to
        fn_bpl = fn
        f_bpl = open(fn_bpl, "w")
        # BPL Document opening tags
        f_bpl.write(xml_opening)
        f_bpl.write(xml_defaults)
        # Start labels
        f_bpl.write(xml_labels)
        n=0
        for lbl in lbls:
            # Start label
            if ( len(lbl.strip()) > 0 ):
                lines = lbl.split(',')
                # Write text tag for each of the three lines
                f_bpl.write('        <!-- LABEL ' + str(n + 1) + ' -->\n')
                n+=1
                f_bpl.write(xml_label)
                txt_height = ['1.42', '1.65', '1.88']
                for i in range(len(lines)):
                    line = lines[i].strip().strip("'")
                    if ( len(line) > 0):
                        f_bpl.write('            <!-- LINE ' + str(i + 1) + ' -->\n')
                        f_bpl.write('            <text position-x="0" position-y="0" align="center" bold="true" font-name="Courier New" >\n')
                        f_bpl.write('                <text-sizing>\n                    <manual height="' + txt_height[i] + '" width="2" font-size="9" />\n                </text-sizing>\n')
                        f_bpl.write('                <datasource>\n                    <static-text value="' + line + '" />\n                </datasource>\n')
                        f_bpl.write('            </text>\n')
                # Close the label tag
                f_bpl.write('        </label>\n')
        # Close labels and document tags
        f_bpl.write('    </labels>\n')
        f_bpl.write('</bpl-document>')
        f_bpl.close()


def GenerateXML():
    root = tk.Tk()
    root.withdraw()

    print("Select the CSV file exported from AutoCAD containing label information...")
    fp_csv = filedialog.askopenfilename()
    fp_csv_sp = ntpath.split(fp_csv)
    fn_csv = fp_csv_sp[1]
    os.chdir(fp_csv_sp[0])

    # Create a BPL file for writing to
    fn_bpl = fn_csv.split('.')
    fn_bpl = fn_bpl[0] + '.xml'
    f_bpl = open(fn_bpl, "w")

    # BPL Document opening tags
    f_bpl.write(xml_opening)
    f_bpl.write(xml_defaults)

    # Open the CSV file and parse labels
    num_lines = sum(1 for line in open(fn_csv))
    print(str(num_lines) + ' labels found for printing.')
    f_csv = open(fn_csv, "r")

    # Start labels
    f_bpl.write(xml_labels)
    for n in range(num_lines):

        # Start label
        label = f_csv.readline()
        if ( len(label.strip()) > 0 ):
            lines = label.split(',')
            # Write text tag for each of the three lines
            f_bpl.write('        <!-- LABEL ' + str(n + 1) + ' -->\n')
            f_bpl.write(xml_label)
            txt_height = ['1.42', '1.65', '1.88']
            for i in range(len(lines)):
                line = lines[i].strip().strip("'")
                if ( len(line) > 0):
                    f_bpl.write('            <!-- LINE ' + str(i + 1) + ' -->\n')
                    f_bpl.write('            <text position-x="0" position-y="0" align="center" bold="true" font-name="Courier New" >\n')
                    f_bpl.write('                <text-sizing>\n                    <manual height="' + txt_height[i] + '" width="2" font-size="9" />\n                </text-sizing>\n')
                    f_bpl.write('                <datasource>\n                    <static-text value="' + line + '" />\n                </datasource>\n')
                    f_bpl.write('            </text>\n')
            # Close the label tag
            f_bpl.write('        </label>\n')

    # Close labels and document tags
    f_bpl.write('    </labels>\n')
    f_bpl.write('</bpl-document>')
    f_bpl.close()
    print('Generated ' + fn_bpl + '.')


def BPL_EnumPrinters():
    rtn_arr = []
    printers = win32print.EnumPrinters(2)
    for p in printers:
        print(p[2])
        rtn_arr.append(p[2])
    return rtn_arr
    

def SendToBP33(fn_bpl, req_confirm = True):

    printer_name = None
    printers = win32print.EnumPrinters(2)
    for p in printers:
        print(p[2])
        if p[2] == 'BBP33':
            printer_name = p[2]
            print('Found printer ' + printer_name)

    if (printer_name):
        cont = 'y'
        if(req_confirm):
            cont = input('Use ' + printer_name + ' to print labels? [y/n]\n')
        if (cont == 'y'):
            f_bpl = open(fn_bpl, "rb")
            hPrinter = win32print.OpenPrinter(printer_name)
            try:
              hJob = win32print.StartDocPrinter (hPrinter, 1, ("Cable labels", None, "RAW"))
              try:
                win32print.StartPagePrinter (hPrinter)
                win32print.WritePrinter (hPrinter, f_bpl.read())
                win32print.EndPagePrinter (hPrinter)
              finally:
                win32print.EndDocPrinter (hPrinter)
            finally:
              win32print.ClosePrinter (hPrinter)
            f_bpl.close()
    else:
        print('Aborted')

def SendToPrinter(printer_name, fn_bpl, req_confirm = True):

    if (printer_name):
        cont = 'y'
        if(req_confirm):
            cont = input('Use ' + printer_name + ' to print labels? [y/n]\n')
        if (cont == 'y'):
            f_bpl = open(fn_bpl, "rb")
            hPrinter = win32print.OpenPrinter(printer_name)
            try:
              hJob = win32print.StartDocPrinter (hPrinter, 1, ("Cable labels", None, "RAW"))
              try:
                win32print.StartPagePrinter (hPrinter)
                win32print.WritePrinter (hPrinter, f_bpl.read())
                win32print.EndPagePrinter (hPrinter)
              finally:
                win32print.EndDocPrinter (hPrinter)
            finally:
              win32print.ClosePrinter (hPrinter)
            f_bpl.close()
    else:
        print('Aborted')