import tkinter as tk
from tkinter import filedialog as fd
import os
import xml.etree.ElementTree as ET

class App(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.grid()
        self.master.title(title)
        

        self.validate_int = (self.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.livesplit_file_button = tk.Button(self, text=livesplit_file_text, command=self.file_dialog)
        self.livesplit_file_button.grid(row=0,column=0)

        self.min_runid_label = tk.Label(self,text="   Min Run ID")
        self.min_runid_label.grid(row=0,column=1)
        self.min_runid_string = tk.StringVar()
        self.min_runid_string.set("0")
        self.min_runid_entry = tk.Entry(self,textvariable=self.min_runid_string,validate="key",validatecommand=self.validate_int,width=5)
        self.min_runid_entry.grid(row=0,column=2)

        self.gametime_check = False
        self.gametime_checkbox = tk.Checkbutton(self,text="GameTime",indicatoron=True, variable=self.gametime_check)
        self.gametime_checkbox.grid(row=0, column=3)

        self.output_textbox = tk.Text(self,width=45)
        self.output_textbox.grid(row=1, column=0, columnspan=4)
        self.output_textbox.insert('1.0',"waiting...")
        

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed == "":
            return True
        if value_if_allowed:
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
        
    def file_dialog(self):
        lss_path = fd.askopenfilename(filetypes=(("LiveSplit Split File", "*.lss"), ("All Files", "*")))
        minID = 0
        try:
            minID = int(self.min_runid_string.get())
        except:
            minID = 0
        try:
            if self.gametime_check:
                self.lss_parse(lss_path, "GameTime", minID)
            else:
                self.lss_parse(lss_path, "RealTime", minID)
        except:
            self.output_textbox.replace('1.0','end',"Error")



    def lss_parse(self, lss_path, timer_mode, min_id):
        lss = ET.parse(lss_path)
        root = lss.getroot()
        attempt_history = {}
        segment_names = {}
        best_segment_run_IDs = {}
        best_times = {}

        for attempt in root.iter("Attempt"):
            attempt_history[attempt.get("id")] = attempt.get("started")
        for segment in root.iter("Segment"):
            best = ""
            name = ""
            run_id = ""
            try:
                best = segment.find("BestSegmentTime").find(timer_mode).text
                name = segment.find("Name").text 
                for time in segment.find("SegmentHistory").iter("Time"):
                    try:
                        if time.find(timer_mode).text == best:
                            run_id = time.get("id")
                    except:
                        next
            except:
                next
            if best != "" and name != "" and run_id != "":
                segment_names[len(segment_names)] = name 
                best_times[len(best_times)] = best
                best_segment_run_IDs[len(best_segment_run_IDs)] = run_id

        count = 0
        out = "Mode: " + timer_mode + "\n"
        while count < len(segment_names):
            if int(best_segment_run_IDs[count]) > min_id:
                out = out + "\n" + segment_names[count] + "\nRun: " + best_segment_run_IDs[count] + " started at: " + attempt_history[best_segment_run_IDs[count]] + " UTC\nSection time: " + best_times[count] + "\n"    
            count += 1
        self.output_textbox.replace('1.0','end',out)



title = "LiveSplit Best Time Parser"
livesplit_file_text = "Browse for Livesplit Splits..."

window = App()
window.mainloop()