import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
import matplotlib 
matplotlib.use("TkAgg")
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import threading
import subprocess
import customtkinter as ctk
from PIL import Image, ImageTk

LARGE_FONT = ("Verdana", 12)
utiliz_file = ""

class CQSimGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = ctk.CTkFrame(self)
        ctk.set_appearance_mode('light')
        self.title('CQSim')
        self.geometry('1000x700')
        self.resizable(False, False)

        # Style the Notebook to look good
        # Create a custom style for the ttk Notebook
        self.style = ttk.Style(self)
        self.style.theme_create('custom_style', parent='alt', settings={
            "TNotebook": {"configure": {"background": "#FBFBFB"}},
            "TNotebook.Tab": {
                "map": {"background": [("selected", '#D6D6D6'), ('!active', '#FBFBFB'), ('active', '#20C6D6')],
                              "expand": [("selected", [1, 1, 1, 0])]}},
                "configure": {"padding": [10,5]}
        })

        # Set the style to the ttk Notebook
        self.style.theme_use('custom_style')

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, RunningPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):
        
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.configure(bg= '#FBFBFB')

        # Parameter Tkinter Vars =======================================================================================
        density_var = tk.DoubleVar(value = 1)
        start_var = tk.DoubleVar(value = 0)
        date_var = tk.StringVar(value = None)
        anchor_var = tk.IntVar(value = 0)
        read_var = tk.IntVar(value = 8000) 
        jsave_var = tk.StringVar()
        nsave_var = tk.StringVar()
        prev_var = tk.StringVar(value = "CQSIM_")
        output_var = tk.StringVar()
        debug_var = tk.StringVar()
        ext_fmtj_var = tk.StringVar(value = ".csv")
        ext_fmtn_var = tk.StringVar(value = ".csv")
        temp_ext_fmtj_var = tk.StringVar(value = ".con")
        temp_ext_fmtn_var = tk.StringVar(value = ".con")
        input_path_var = tk.StringVar(value = "InputFiles/")
        output_path_var = tk.StringVar(value = "Results/")
        temp_result_path_var = tk.StringVar(value = "Temp/")
        debug_path_var = tk.StringVar(value = "Debug/")
        ext_jr_var = tk.StringVar(value = ".rst")
        ext_si_var = tk.StringVar(value = ".ult")
        ext_ai_var = tk.StringVar(value = ".adp")
        ext_d_var = tk.StringVar(value = ".log") 
        debug_lvl_var = tk.IntVar(value = 4)
        alg_list_var = tk.StringVar(value = None)
        alg_adapt_var = tk.IntVar(value = 0)
        alg_sign_var = tk.StringVar(value = None)
        alg_adapt_list_var = tk.StringVar(value = None)
        backfill_var = tk.IntVar(value = 0)
        backfill_para_var = tk.StringVar(value = None)
        backfill_adapt_var = tk.IntVar(value = 0)
        backfill_adapt_para_var = tk.StringVar(value = None)
        window_mode_var = tk.IntVar(value = 0)
        window_para_list_var = tk.StringVar(value = None)
        window_adapt_var = tk.IntVar(value = 0)
        window_adapt_para_var = tk.StringVar(value = None)
        config_file_var = tk.StringVar(value = "config_n.set")
        config_sys_var = tk.StringVar(value = "config_sys.set")
        monitor_interval_var = tk.IntVar(value = None)
        monitor_para_var = tk.StringVar(value = None)
        uti_var = tk.StringVar(value = None)
        ver_var = tk.StringVar(value = "ORG")

        self.job_name_var = tk.StringVar(value = None)


        # Title ========================================================================================================

        # Load the image
        image_path = "cqsim-logo.jpg"  # Replace "your_image.jpg" with the actual image filename
        image = Image.open(image_path).resize((450,150))
        self.photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        self.image_label = tk.Label(self, borderwidth=0, highlightthickness=0)
        self.image_label.image = self.photo
        self.image_label.configure(image=self.photo)
        self.image_label.pack()



        # Select Job and Node Trace Buttons Frame ======================================================================
        select_frame = ctk.CTkFrame(master = self, fg_color = 'transparent')
        select_frame.pack(fill= 'x')

        # select_text = ctk.CTkLabel(select_frame, text = 'Select Job Trace and Node Trace', font = ('Arial', 20))
        # select_text.pack(pady = 15)

        # Select Job/Node File Fucntions
        def get_job():
            filetypes = (   
                ('Standard Worload Format', '*.swf'),
                ('All files', '*.*')
            )

            file_path = fd.askopenfilename(title = 'Select Trace', filetypes=filetypes, initialdir='~/CQSim/data/InputFiles')
            job_var.set(os.path.basename(file_path))

            if checked_bool.get():
                node_var.set(os.path.basename(str(file_path)))

            name = job_var.get().replace(".swf", "")
            
            jsave_var.set(name)
            nsave_var.set("" + name + "_node" )
            output_var.set(name)
            debug_var.set("debug_" + name)
            self.job_name_var.set(name)

        def get_node():
            filetypes = (   
                ('Standard Worload Format', '*.swf'),
                ('All files', '*.*')
            )

            file_path = fd.askopenfilename(title = 'Select Trace', filetypes=filetypes, initialdir='~/CQSim/data/InputFiles')
            node_var.set(os.path.basename(str(file_path)))

            if checked_bool.get():
                job_var.set(os.path.basename(str(file_path)))
                name = job_var.get().replace(".swf", "")
            
                jsave_var.set(name)
                nsave_var.set("" + name + "_node" )
                output_var.set(name)
                debug_var.set("debug_" + name)
                self.job_name_var.set(name)

        # Select Frame setup
        job_frame = ctk.CTkFrame(select_frame, fg_color = 'transparent')
        node_frame = ctk.CTkFrame(select_frame, fg_color = 'transparent')
        check_frame = ctk.CTkFrame(select_frame, fg_color = 'transparent')

        job_frame.pack  (side='left', expand=True, fill='both', padx = 20)
        check_frame.pack(side='left', expand=True, fill='both')
        node_frame.pack (side='left', expand=True, fill='both', padx = 20)

        # Job Frame
        job_var = tk.StringVar()

        job_title = ctk.CTkLabel(job_frame, text = 'Job Trace', font = ('Arial', 12))
        job_button = ctk.CTkButton(job_frame, text = 'Select Job Trace', command = get_job, fg_color='#20C6D6', text_color='black')
        job_label = ctk.CTkLabel(job_frame, textvariable = job_var)

        # Job layout
        job_title.pack()
        job_button.pack(expand = True)
        job_label.pack()

        # Checkbox Frame
        checked_bool = tk.BooleanVar(value = False)

        def same_file():
            if checked_bool.get():
                node_var.set(job_var.get()) if len(job_var.get()) > 0 else job_var.set(node_var.get())

        check_label = ctk.CTkLabel(check_frame, text = 'Check if Job and Node can use the same file')
        same_file = ctk.CTkCheckBox(check_frame, command = same_file, variable=checked_bool)
        same_file.configure(text='')

        # Checkbox layout
        check_label.pack()
        same_file.pack(side='right', padx = 160)

        # Node Frame
        node_var = tk.StringVar()

        node_title = ctk.CTkLabel(node_frame, text = 'Node Structure', font = ('Arial', 12))
        node_button = ctk.CTkButton(node_frame, text = 'Select Node Structure', command = get_node, fg_color='#20C6D6', text_color='black')
        node_label = ctk.CTkLabel(node_frame, textvariable = node_var)

        # Node layout
        node_title.pack()
        node_button.pack(expand= True)
        node_label.pack()

        # Start of Notebook Tabs  ======================================================================================

        notebook = ttk.Notebook(self)

        # Tab 0 GRAPH Frame -------------------------------------------------------------------------------
        self.graph_var = tk.StringVar()
        self.graph_var.set("0")
        
        Tab0 = ctk.CTkFrame(notebook, width=900, height=200, bg_color='#FBFBFB')

        text = ctk.CTkLabel(Tab0, text = "Select Run Time Graph Analysis", font = ('Elephant', 20))

        t0_left = ctk.CTkFrame(Tab0, fg_color = 'transparent')
        t0_middle = ctk.CTkFrame(Tab0, fg_color = 'transparent')
        t0_right = ctk.CTkFrame(Tab0, fg_color = 'transparent')

        util_graph_label = ctk.CTkLabel(t0_left, text = "Utilization Graph",font = ('Elephant', 15))
        util_button = ctk.CTkRadioButton(t0_left, value = '0', text = '', variable=self.graph_var, )

        max_wait_label = ctk.CTkLabel(t0_middle, text = "Max Job Wait Time",font = ('Elephant', 15))
        max_wait_button = ctk.CTkRadioButton(t0_middle, value = '1', text='', variable=self.graph_var)

        avg_wait_label = ctk.CTkLabel(t0_right, text = "Average Job Wait Time",font = ('Elephant', 15))
        avg_wait_button = ctk.CTkRadioButton(t0_right, value = '2', text= '', variable=self.graph_var)

        # Tab 0 GRAPH Layout ------------------------------------------------------------------------------

        text.pack(pady = 10)
        t0_left.pack(side = 'left', pady= 30, expand=True, fill='both')
        t0_middle.pack(side = 'left', pady= 30, expand=True, fill='both')
        t0_right.pack(side = 'left', pady= 30, expand=True, fill='both')

        util_graph_label.pack(pady = 5)
        # util_button.pack(padx = 50, expand = True, fill='both')
        util_button.place(anchor = 'center', relx =.64, rely =.4)

        max_wait_label.pack(pady = 5)
        # max_wait_button.pack(padx = 50, expand = True, fill='both')
        max_wait_button.place(anchor = 'center', relx =.64, rely =.4)

        avg_wait_label.pack(pady = 5)
        # avg_wait_button.pack(padx = 50, expand = True, fill = 'both')
        avg_wait_button.place(anchor = 'center', relx =.64, rely =.4)

        # Tab 1 JOB TRACE Frame ---------------------------------------------------------------------------
        Tab1 = ctk.CTkFrame(notebook, width=900, height=200, bg_color='#FBFBFB')

        t1_top = ctk.CTkFrame(Tab1, fg_color = 'transparent')
        t1_bottom = ctk.CTkFrame(Tab1, fg_color = 'transparent')
        t1_top_left = ctk.CTkFrame(t1_top, fg_color = 'transparent')
        t1_top_right = ctk.CTkFrame(t1_top, fg_color = 'transparent')
        density_frame = ctk.CTkFrame(t1_top_left, fg_color = 'transparent')
        start_frame = ctk.CTkFrame(t1_top_right, fg_color = 'transparent')
        date_frame = ctk.CTkFrame(t1_top_right, fg_color = 'transparent')
        anchor_frame = ctk.CTkFrame(t1_top_left, fg_color = 'transparent')

        density_label = ctk.CTkLabel(density_frame, text = 'Job Density:')
        density = ctk.CTkEntry(density_frame, justify='center', textvariable = density_var)

        start_label = ctk.CTkLabel(start_frame, text='Start Time:')
        start = ctk.CTkEntry(start_frame, justify='center', textvariable = start_var)

        date_label = ctk.CTkLabel(date_frame, text = 'Start Date:')
        date = ctk.CTkEntry(date_frame, justify='center', textvariable = date_var)

        anchor_label = ctk.CTkLabel(anchor_frame, text = 'First Job Position:')
        anchor = ctk.CTkEntry(anchor_frame, justify='center', textvariable = anchor_var)

        read_label = ctk.CTkLabel(t1_bottom, text = 'Number of Jobs Read From Job Trace:')
        read = ctk.CTkEntry(t1_bottom, justify='center', textvariable = read_var)

        # Tab 1 JOB TRACE Layout
        t1_top.pack(pady = 10)
        t1_bottom.pack(pady=10)
        t1_top_left.pack(side = 'left')
        t1_top_right.pack(side = 'left')
        density_frame.pack(pady= 10, padx=100)
        start_frame.pack(pady= 10, padx=100)
        date_frame.pack(pady= 10, padx=100)
        anchor_frame.pack(pady= 10, padx=100)

        density_label.pack(anchor='center')
        density.pack(anchor='center')

        anchor_label.pack(anchor='center')
        anchor.pack(anchor='center')

        start_label.pack(anchor='center')
        start.pack(anchor='center')

        date_label.pack(anchor='center')
        date.pack(anchor='center')

        read_label.pack()
        read.pack()


        # Tab 2 FILES Frame -------------------------------------------------------------------------------
        Tab2 = ctk.CTkFrame(notebook, width=900, height=200)

        t2_top = ctk.CTkFrame(Tab2, fg_color = 'transparent')
        t2_bottom = ctk.CTkFrame(Tab2, fg_color = 'transparent')
        t2_top_left = ctk.CTkFrame(t2_top, fg_color = 'transparent')
        t2_top_right = ctk.CTkFrame(t2_top, fg_color = 'transparent')
        jsave_frame = ctk.CTkFrame(t2_top_left, fg_color = 'transparent')
        nsave_frame = ctk.CTkFrame(t2_top_left, fg_color = 'transparent')
        prev_frame = ctk.CTkFrame(t2_top_right, fg_color = 'transparent')
        output_frame = ctk.CTkFrame(t2_top_right, fg_color = 'transparent')

        jsave_label = ctk.CTkLabel(jsave_frame, text = 'Formatted Job Trace Data Name:')
        jsave = ctk.CTkEntry(jsave_frame, justify='center', textvariable = jsave_var)

        nsave_label = ctk.CTkLabel(nsave_frame, text = 'Formatted Node Data Name:')
        nsave = ctk.CTkEntry(nsave_frame, justify='center', textvariable = nsave_var)

        prev_label = ctk.CTkLabel(prev_frame, text = 'Previous File Name:')
        prev = ctk.CTkEntry(prev_frame, justify='center', textvariable = prev_var)

        output_label =ctk.CTkLabel(output_frame, text = 'Simulate Result File Name:')
        output = ctk.CTkEntry(output_frame, justify='center', textvariable = output_var)

        debug_label = ctk.CTkLabel(t2_bottom, text = 'Debug File Name:')
        debug = ctk.CTkEntry(t2_bottom, justify='center', textvariable = debug_var)

        # Tab 2 FILES Layout
        t2_top.pack(pady = 10)
        t2_bottom.pack(pady=10)
        t2_top_left.pack(side = 'left')
        t2_top_right.pack(side = 'left')
        jsave_frame.pack(pady= 10, padx=100)
        nsave_frame.pack(pady= 10, padx=100)
        prev_frame.pack(pady= 10, padx=100)
        output_frame.pack(pady= 10, padx=100)

        jsave_label.pack(anchor='center')
        jsave.pack(anchor='center')

        nsave_label.pack(anchor='center')
        nsave.pack(anchor='center')

        prev_label.pack(anchor='center')
        prev.pack(anchor='center')

        output_label.pack(anchor='center')
        output.pack(anchor='center')

        debug_label.pack(anchor='center')
        debug.pack(anchor='center')


        # Tab 3 FMT Frames --------------------------------------------------------------------------------
        Tab3 = ctk.CTkFrame(notebook, width=900, height=200)

        t3_top = ctk.CTkFrame(Tab3, fg_color = 'transparent')
        t3_bottom = ctk.CTkFrame(Tab3, fg_color = 'transparent')
        t3_top_left = ctk.CTkFrame(t3_top, fg_color = 'transparent')
        t3_top_right = ctk.CTkFrame(t3_top, fg_color = 'transparent')
        t3_bot_left = ctk.CTkFrame(t3_bottom, fg_color = 'transparent')
        t3_bot_right = ctk.CTkFrame(t3_bottom, fg_color = 'transparent')


        ext_fmtj_label = ctk.CTkLabel(t3_top_left, text = 'Formatted Job Data Ext:')
        ext_fmtj = ctk.CTkEntry(t3_top_left, justify='center', textvariable = ext_fmtj_var)

        ext_fmtn_label = ctk.CTkLabel(t3_top_right, text = 'Formatted Node Data Ext:')
        ext_fmtn = ctk.CTkEntry(t3_top_right, justify='center', textvariable = ext_fmtn_var)

        temp_ext_fmtj_label = ctk.CTkLabel(t3_bot_left, text = 'Temp Job Trace Config Ext:')
        temp_ext_fmtj = ctk.CTkEntry(t3_bot_left, justify='center', textvariable = temp_ext_fmtj_var)

        temp_ext_fmtn_label = ctk.CTkLabel(t3_bot_right, text = 'Temp Node Struct Config Ext:')
        temp_ext_fmtn = ctk.CTkEntry(t3_bot_right, justify='center', textvariable = temp_ext_fmtn_var)

        # Tab 3 FMT Layout
        t3_top.pack(pady = 10)
        t3_bottom.pack(pady=10)
        t3_top_left.pack(side = 'left',pady= 10, padx=90, expand=True, fill='both')
        t3_top_right.pack(side = 'left',pady= 10, padx=90, expand=True, fill='both')
        t3_bot_left.pack(side = 'left', pady= 10, padx=80, expand=True, fill='both')
        t3_bot_right.pack(side = 'left', pady= 10, padx=80, expand=True, fill='both')


        ext_fmtj_label.pack(anchor='center')
        ext_fmtj.pack(anchor='center')

        ext_fmtn_label.pack(anchor='center')
        ext_fmtn.pack(anchor='center')

        temp_ext_fmtj_label.pack(anchor='center')
        temp_ext_fmtj.pack(anchor='center')

        temp_ext_fmtn_label.pack(anchor='center', expand= True)
        temp_ext_fmtn.pack(anchor='center')


        # Tab 4 PATHS Frames ------------------------------------------------------------------------------
        Tab4 = ctk.CTkFrame(notebook, width=900, height=200)

        t4_top = ctk.CTkFrame(Tab4, fg_color = 'transparent')
        t4_bottom = ctk.CTkFrame(Tab4, fg_color = 'transparent')
        t4_top_left = ctk.CTkFrame(t4_top, fg_color = 'transparent')
        t4_top_right = ctk.CTkFrame(t4_top, fg_color = 'transparent')
        t4_bot_left = ctk.CTkFrame(t4_bottom, fg_color = 'transparent')
        t4_bot_right = ctk.CTkFrame(t4_bottom, fg_color = 'transparent')

        input_path_label = ctk.CTkLabel(t4_top_left, text = 'Input File Path:')
        input_path = ctk.CTkEntry(t4_top_left, justify='center', textvariable = input_path_var)

        output_path_label = ctk.CTkLabel(t4_top_right, text = 'Output Result File Path:')
        output_path = ctk.CTkEntry(t4_top_right, justify='center', textvariable = output_path_var)

        temp_result_path_label = ctk.CTkLabel(t4_bot_left, text = 'Temp Result File Path:')
        temp_result_path = ctk.CTkEntry(t4_bot_left, justify='center', textvariable = temp_result_path_var)

        debug_path_label = ctk.CTkLabel(t4_bot_right, text = 'Debug File Path:')
        debug_path = ctk.CTkEntry(t4_bot_right, justify='center', textvariable = debug_path_var)

        # Tab 4 PATHS Layout
        t4_top.pack(pady = 10)
        t4_bottom.pack(pady=10)
        t4_top_left.pack(side = 'left',pady= 10, padx=100)
        t4_top_right.pack(side = 'left',pady= 10, padx=100)
        t4_bot_left.pack(side = 'left', pady= 10, padx=100)
        t4_bot_right.pack(side = 'left', pady= 10, padx=100)

        input_path_label.pack(anchor='center')
        input_path.pack(anchor='center')

        output_path_label.pack(anchor='center')
        output_path.pack(anchor='center')

        temp_result_path_label.pack(anchor='center')
        temp_result_path.pack(anchor='center')

        debug_path_label.pack(anchor='center')
        debug_path.pack(anchor='center')


        # Tab 5 EXTENSIONS Frames -------------------------------------------------------------------------
        Tab5 = ctk.CTkFrame(notebook, width=900, height=200)

        t5_top = ctk.CTkFrame(Tab5, fg_color = 'transparent')
        t5_bottom = ctk.CTkFrame(Tab5, fg_color = 'transparent')
        t5_top_left = ctk.CTkFrame(t5_top, fg_color = 'transparent')
        t5_top_right = ctk.CTkFrame(t5_top, fg_color = 'transparent')
        t5_bot_left = ctk.CTkFrame(t5_bottom, fg_color = 'transparent')
        t5_bot_right = ctk.CTkFrame(t5_bottom, fg_color = 'transparent')

        ext_jr_label = ctk.CTkLabel(t5_top_left, text = 'Job Result Log Ext:')
        ext_jr = ctk.CTkEntry(t5_top_left, justify='center', textvariable = ext_jr_var)

        ext_si_label = ctk.CTkLabel(t5_top_right, text = 'System Info Log Ext:')
        ext_si = ctk.CTkEntry(t5_top_right, justify='center', textvariable = ext_si_var)

        ext_ai_label = ctk.CTkLabel(t5_bot_left, text = 'Adapt Info Log Ext:')
        ext_ai = ctk.CTkEntry(t5_bot_left, justify='center', textvariable = ext_ai_var)

        ext_d_label = ctk.CTkLabel(t5_bot_right, text = 'Debug Log Ext:')
        ext_d = ctk.CTkEntry(t5_bot_right, justify='center', textvariable = ext_d_var)

        # Tab 5 EXTENSIONS Layout 

        t5_top.pack(pady = 10)
        t5_bottom.pack(pady=10)
        t5_top_left.pack(side = 'left',pady= 10, padx=100)
        t5_top_right.pack(side = 'left',pady= 10, padx=100)
        t5_bot_left.pack(side = 'left', pady= 10, padx=100)
        t5_bot_right.pack(side = 'left', pady= 10, padx=100)


        ext_jr_label.pack(anchor='center')
        ext_jr.pack(anchor='center')

        ext_si_label.pack(anchor='center')
        ext_si.pack(anchor='center')

        ext_ai_label.pack(anchor='center')
        ext_ai.pack(anchor='center')

        ext_d_label.pack(anchor='center')
        ext_d.pack(anchor='center')


        # Tab 6 DEBUG Frames ------------------------------------------------------------------------------
        Tab6 = ctk.CTkFrame(notebook, width=900, height=200)

        t6_left = ctk.CTkFrame(Tab6, fg_color = 'transparent')
        t6_right = ctk.CTkFrame(Tab6, fg_color = 'transparent')

        debug_label2 = ctk.CTkLabel(t6_left, text = 'Debug File Name:')
        debug2 = ctk.CTkEntry(t6_left, justify='center', textvariable = debug_var)

        debug_lvl_label = ctk.CTkLabel(t6_right, text = 'Debug Level:')
        debug_lvl = ctk.CTkEntry(t6_right, justify='center', textvariable = debug_lvl_var)

        # Tab 6 DEBUG Layout
        t6_left.pack(side = 'left', pady= 70, padx=100, expand=True, fill='both')
        t6_right.pack(side = 'left', pady= 70, padx=100, expand=True, fill='both')

        debug_label2.pack(anchor='center')
        debug2.pack(anchor='center')

        debug_lvl_label.pack(anchor='center')
        debug_lvl.pack(anchor='center')


        # Tab 7 ALGORITHM Frames -------------------------------------------------------------------------- 
        Tab7 = ctk.CTkFrame(notebook, width=900, height=200)

        t7_top = ctk.CTkFrame(Tab7, fg_color = 'transparent')
        t7_bottom = ctk.CTkFrame(Tab7, fg_color = 'transparent')
        t7_top_left = ctk.CTkFrame(t7_top, fg_color = 'transparent')
        t7_top_right = ctk.CTkFrame(t7_top, fg_color = 'transparent')
        t7_bot_left = ctk.CTkFrame(t7_bottom, fg_color = 'transparent')
        t7_bot_right = ctk.CTkFrame(t7_bottom, fg_color = 'transparent')

        alg_list_label = ctk.CTkLabel(t7_top_left, text = 'Basic Algorithm List:')
        alg_list = ctk.CTkEntry(t7_top_left, justify='center', textvariable = alg_list_var)

        alg_adapt_label = ctk.CTkLabel(t7_top_right, text = 'Algorithm Adapt Mode:')
        alg_adapt = ctk.CTkEntry(t7_top_right, justify='center', textvariable = alg_adapt_var)

        alg_sign_label = ctk.CTkLabel(t7_bot_left, text = 'Sign of Basic Algoithm List:')
        alg_sign = ctk.CTkEntry(t7_bot_left, justify='center', textvariable = alg_sign_var)

        alg_adapt_list_label = ctk.CTkLabel(t7_bot_right, text = 'Algorithm Adapt Parameter List:')
        alg_adapt_list = ctk.CTkEntry(t7_bot_right, justify='center', textvariable = alg_adapt_list_var)

        # Tab 7 ALGORITHIM Layout
        t7_top.pack(pady = 10)
        t7_bottom.pack(pady=10)
        t7_top_left.pack(side = 'left',pady= 10, padx=100)
        t7_top_right.pack(side = 'left',pady= 10, padx=100)
        t7_bot_left.pack(side = 'left', pady= 10, padx=100)
        t7_bot_right.pack(side = 'left', pady= 10, padx=100)

        alg_list_label.pack(anchor='center')
        alg_list.pack(anchor='center') 

        alg_adapt_label.pack(anchor='center') 
        alg_adapt.pack(anchor='center')

        alg_sign_label.pack(anchor='center')
        alg_sign.pack(anchor='center')

        alg_adapt_list_label.pack(anchor='center')
        alg_adapt_list.pack(anchor='center')


        # Tab 8 BACKFILLING Frames ------------------------------------------------------------------------
        Tab8 = ctk.CTkFrame(notebook, width=900, height=200)

        t8_top = ctk.CTkFrame(Tab8, fg_color = 'transparent')
        t8_bottom = ctk.CTkFrame(Tab8, fg_color = 'transparent')
        t8_top_left = ctk.CTkFrame(t8_top, fg_color = 'transparent')
        t8_top_right = ctk.CTkFrame(t8_top, fg_color = 'transparent')
        t8_bot_left = ctk.CTkFrame(t8_bottom, fg_color = 'transparent')
        t8_bot_right = ctk.CTkFrame(t8_bottom, fg_color = 'transparent')

        backfill_label = ctk.CTkLabel(t8_top_left, text = 'Backfill Mode:')
        backfill = ctk.CTkEntry(t8_top_left, justify='center', textvariable = backfill_var)

        backfill_para_label = ctk.CTkLabel(t8_top_right, text = 'Backfill Parameter List:')
        backfill_para = ctk.CTkEntry(t8_top_right, justify='center', textvariable = backfill_para_var)

        backfill_adapt_label = ctk.CTkLabel(t8_bot_left, text = 'Backfill Adapt Mode:')
        backfill_adapt = ctk.CTkEntry(t8_bot_left, justify='center', textvariable = backfill_adapt_var)

        backfill_adapt_para_label = ctk.CTkLabel(t8_bot_right, text = 'Backfill Adapt Parameter List:')
        backfill_adapt_para = ctk.CTkEntry(t8_bot_right, justify='center', textvariable = backfill_adapt_para_var)

        # Tab 8 BACKFILLING Layout
        t8_top.pack(pady = 10)
        t8_bottom.pack(pady=10)
        t8_top_left.pack(side = 'left',pady= 10, padx=100)
        t8_top_right.pack(side = 'left',pady= 10, padx=100)
        t8_bot_left.pack(side = 'left', pady= 10, padx=100)
        t8_bot_right.pack(side = 'left', pady= 10, padx=100)

        backfill_label.pack(anchor='center')
        backfill.pack(anchor='center')

        backfill_para_label.pack(anchor='center')
        backfill_para.pack(anchor='center')

        backfill_adapt_label.pack(anchor='center')
        backfill_adapt.pack(anchor='center')

        backfill_adapt_para_label.pack(anchor='center')
        backfill_adapt_para.pack(anchor='center')


        # Tab 9 WINDOW Frames -----------------------------------------------------------------------------
        Tab9 = ctk.CTkFrame(notebook, width=900, height=200)

        t9_top = ctk.CTkFrame(Tab9, fg_color = 'transparent')
        t9_bottom = ctk.CTkFrame(Tab9, fg_color = 'transparent')
        t9_top_left = ctk.CTkFrame(t9_top, fg_color = 'transparent')
        t9_top_right = ctk.CTkFrame(t9_top, fg_color = 'transparent')
        t9_bot_left = ctk.CTkFrame(t9_bottom, fg_color = 'transparent')
        t9_bot_right = ctk.CTkFrame(t9_bottom, fg_color = 'transparent')

        window_mode_label = ctk.CTkLabel(t9_top_left, text = 'Window Mode:')
        window_mode = ctk.CTkEntry(t9_top_left, justify='center', textvariable = window_mode_var)

        window_para_list_label = ctk.CTkLabel(t9_top_right, text = 'Window Parameter List:')
        window_para_list  = ctk.CTkEntry(t9_top_right, justify='center', textvariable = window_para_list_var)

        window_adapt_label = ctk.CTkLabel(t9_bot_left, text = 'Window Adapt Mode:')
        window_adapt = ctk.CTkEntry(t9_bot_left, justify='center', textvariable = window_adapt_var)

        window_adapt_para_label = ctk.CTkLabel(t9_bot_right, text = 'Window Adapt Parameter List:')
        window_adapt_para = ctk.CTkEntry(t9_bot_right, justify='center', textvariable = window_adapt_para_var)

        # Tab 9 WINDOW Layout 
        t9_top.pack(pady = 10)
        t9_bottom.pack(pady=10)
        t9_top_left.pack(side = 'left',pady= 10, padx=100)
        t9_top_right.pack(side = 'left',pady= 10, padx=100)
        t9_bot_left.pack(side = 'left', pady= 10, padx=100)
        t9_bot_right.pack(side = 'left', pady= 10, padx=100)

        window_mode_label.pack(anchor='center')
        window_mode.pack(anchor='center')

        window_para_list_label.pack(anchor='center')
        window_para_list.pack(anchor='center')

        window_adapt_label.pack(anchor='center')
        window_adapt.pack(anchor='center')

        window_adapt_para_label.pack(anchor='center')
        window_adapt_para.pack(anchor='center')


        # Tab 10 CONFIG Frames ----------------------------------------------------------------------------
        Tab10 = ctk.CTkFrame(notebook, width=900, height=200)

        t10_left = ctk.CTkFrame(Tab10, fg_color = 'transparent')
        t10_right = ctk.CTkFrame(Tab10, fg_color = 'transparent')

        config_file_label = ctk.CTkLabel(t10_left, text = 'Config File:')
        config_file = ctk.CTkEntry(t10_left, justify='center', textvariable = config_file_var)

        config_sys_label = ctk.CTkLabel(t10_right, text = 'System Config File:')
        config_sys = ctk.CTkEntry(t10_right, justify='center', textvariable = config_sys_var)

        # Tab 10 CONFIG Layout
        t10_left.pack(side = 'left', pady= 70, padx=100, expand=True, fill='both')
        t10_right.pack(side = 'left', pady= 70, padx=100, expand=True, fill='both')

        config_file_label.pack(anchor='center')
        config_file.pack(anchor='center')

        config_sys_label.pack(anchor='center')
        config_sys.pack(anchor='center')

        # Tab 11 MONITOR Frames ---------------------------------------------------------------------------
        Tab11 = ctk.CTkFrame(notebook, width=900, height=200)

        t11_left = ctk.CTkFrame(Tab11, fg_color = 'transparent')
        t11_right = ctk.CTkFrame(Tab11, fg_color = 'transparent')

        monitor_interval_label = ctk.CTkLabel(t11_left, text = 'Monitor Interval Time:')
        monitor_interval = ctk.CTkEntry(t11_left, justify='center', textvariable = monitor_interval_var)

        monitor_para_label = ctk.CTkLabel(t11_right, text = 'Monitor Parameter List:')
        monitor_para = ctk.CTkEntry(t11_right, justify='center', textvariable = monitor_para_var)

        # Tab 11 MONITOR Layout

        t11_left.pack(side = 'left', pady= 70, padx=100, expand=True, fill='both')
        t11_right.pack(side = 'left', pady= 70, padx=100, expand=True, fill='both')

        monitor_interval_label.pack(anchor='center')
        monitor_interval.pack(anchor='center')

        monitor_para_label.pack(anchor='center')
        monitor_para.pack(anchor='center')

        # Tab 12 MISC Frames ------------------------------------------------------------------------------
        Tab12 = ctk.CTkFrame(notebook, width=900, height=200)

        t12_left = ctk.CTkFrame(Tab12, fg_color = 'transparent')
        t12_right = ctk.CTkFrame(Tab12, fg_color = 'transparent')

        uti_label = ctk.CTkLabel(t12_left, text = 'Avg Utilization Interval List:')
        uti = ctk.CTkEntry(t12_left, justify='center', textvariable = uti_var)

        ver_label = ctk.CTkLabel(t12_right, text = 'Version Name:')
        ver = ctk.CTkEntry(t12_right, justify='center', textvariable = ver_var)

        # Tab 12 MISC Layout
        t12_left.pack(side = 'left', pady= 70, padx=100, expand=True, fill='both')
        t12_right.pack(side = 'left', pady= 70, padx=100, expand=True, fill='both')

        uti_label.pack(anchor='center')
        uti.pack(anchor='center')

        ver_label.pack(anchor='center')
        ver.pack(anchor='center')


        # Notebook layout ---------------------------------------------------------------------------------

        notebook.add(Tab0, text = 'GRAPH')
        notebook.add(Tab1, text = 'JOB TRACE')
        notebook.add(Tab2, text = 'FILES')
        notebook.add(Tab3, text = 'FMT')
        notebook.add(Tab4, text = 'PATHS')
        notebook.add(Tab5, text = 'EXTENSIONS')
        notebook.add(Tab6, text = 'DEBUG')
        notebook.add(Tab7, text = 'ALGORITHM')
        notebook.add(Tab8, text = 'BACKFILLING')
        notebook.add(Tab9, text = 'WINDOW')
        notebook.add(Tab10, text = 'CONFIG')
        notebook.add(Tab11, text = 'MONITOR')
        notebook.add(Tab12, text = 'MISC')


        notebook.pack(fill='x', padx=50, pady=25)

        # Run Button Functions ============================================================================

        # Function checks to see if any of the parameters are different than the default. 
        def format_parameters():

            para_list = []

            # Just a large if statement to check if these variables have changed
            if (job_var.get()):
                temp = "-j " + job_var.get()
                para_list.append(temp)

            if (node_var.get()):
                temp = "-n " + node_var.get()
                para_list.append(temp)

            if (density_var.get() != 1):
                temp = "-f " + str(density_var.get())
                para_list.append(temp)

            if (start_var.get() != 0):
                temp = "-s " + str(start_var.get())
                para_list.append(temp)

            if (date_var.get()):
                temp = "-S " + str(date_var.get())
                para_list.append(temp)

            if (anchor_var.get() != 0):
                temp = "-r " + str(anchor_var.get())
                para_list.append(temp)

            if (read_var.get() != 8000):
                temp = "-R " + str(read_var.get())
                para_list.append(temp)


            if (jsave_var.get()):
                if not (job_var.get()):
                    temp = "-J " + jsave_var.get()
                    para_list.append(temp)
                else:
                    name = job_var.get().replace(".swf", "")
                    if (jsave_var.get() != name):
                        temp = "-J " + jsave_var.get()
                        para_list.append(temp)


            if (nsave_var.get()):
                if not (job_var.get()):
                    temp = "-N " + nsave_var.get()
                    para_list.append(temp)
                else:
                    name = job_var.get().replace(".swf", "") + "_node"
                    if (nsave_var.get() != name):
                        temp = "-N " + nsave_var.get()
                        para_list.append(temp)

            if (prev_var.get() != "CQSIM_"):
                temp = "-p " + prev_var.get()
                para_list.append(temp)
            
            if (output_var.get()):
                if not (job_var.get()):
                    temp = "-o " + output_var.get()
                    para_list.append(temp)
                else:
                    name = job_var.get().replace(".swf", "")
                    if (output_var.get() != name):
                        temp = "-o " + output_var.get()
                        para_list.append(temp)
            
            if (debug_var.get()):
                if not (job_var.get()):
                    temp = "--debug " + debug_var.get()
                    para_list.append(temp)
                else:
                    name = "debug_" + job_var.get().replace(".swf", "")
                    if (debug_var.get() != name):
                        temp = "--debug " + debug_var.get()
                        para_list.append(temp)

            if (ext_fmtj_var.get() != ".csv"):
                temp = "--ext_fmt_j " + ext_fmtj_var.get()
                para_list.append(temp)

            if (ext_fmtn_var.get() != ".csv"):
                temp = "--ext_fmt_n " + ext_fmtn_var.get()
                para_list.append(temp)
        
            if (temp_ext_fmtj_var.get() != ".con"):
                temp = "--ext_fmt_j_c " + temp_ext_fmtj_var.get()
                para_list.append(temp)

            if (temp_ext_fmtn_var.get() != ".con"):
                temp = "--ext_fmt_n_c " + temp_ext_fmtn_var.get()
                para_list.append(temp)

            if (input_path_var.get() != "InputFiles/"):
                temp = "--path_in " + input_path_var.get()
                para_list.append(temp)

            if (output_path_var.get() != "Results/"):
                temp = "--path_out " + output_path_var.get()
                para_list.append(temp)

            if (temp_result_path_var.get() != "Temp/"):
                temp = "--path_tmp " + temp_result_path_var.get()
                para_list.append(temp)

            if (debug_path_var.get() != "Debug/"):
                temp = "--path_debug " + debug_path_var.get()
                para_list.append(temp)

            if (ext_jr_var.get() != ".rst"):
                temp = "--ext_jr " + ext_jr_var.get()
                para_list.append(temp)

            if (ext_si_var.get() != ".ult"):
                temp = "--ext_si " + ext_si_var.get()
                para_list.append(temp)

            if (ext_ai_var.get() != ".adp"):
                temp = "--ext_ai " + ext_ai_var.get()
                para_list.append(temp)

            if (ext_d_var.get() != ".log"):
                temp = "--ext_d " + ext_d_var.get()
                para_list.append(temp)

            if (debug_lvl_var.get() != 4):
                temp = "-v " + str(debug_lvl_var.get())
                para_list.append(temp)

            if (alg_list_var.get()):
                temp = "--alg " + alg_list_var.get()
                para_list.append(temp)

            if (alg_adapt_var.get() != 0):
                temp = "-g " + str(alg_adapt_var.get())
                para_list.append(temp)

            if (alg_sign_var.get()):
                temp = "-A " + alg_sign_var.get()
                para_list.append(temp)

            if (alg_adapt_list_var.get()):
                temp = "-G " + alg_adapt_list_var.get()
                para_list.append(temp)

            if (backfill_var.get() != 0):
                temp = "-b " + str(backfill_var.get())
                para_list.append(temp)

            if (backfill_para_var.get()):
                temp = "-B " + backfill_para_var.get()
                para_list.append(temp)

            if (backfill_adapt_var.get() != 0):
                temp = "-I " + str(backfill_adapt_var.get())
                para_list.append(temp)

            if (backfill_adapt_para_var.get()):
                temp = "-L " + backfill_adapt_para_var.get()
                para_list.append(temp)

            if (window_mode_var.get() != 0):
                temp = "-w " + str(window_mode_var.get())
                para_list.append(temp)

            if (window_para_list_var.get()):
                temp = "-W " + window_para_list_var.get()
                para_list.append(temp)

            if (window_adapt_var.get() != 0):
                temp = "-d " + str(window_adapt_var.get())
                para_list.append(temp)

            if (window_adapt_para_var.get()):
                temp = "-D " + window_adapt_para_var.get()
                para_list.append(temp)

            if (config_file_var.get() != "config_n.set"):
                temp = "-c " + config_file_var.get()
                para_list.append(temp)

            if (config_sys_var.get() != "config_sys.set"):
                temp = "-C " + config_sys_var.get()
                para_list.append(temp)

            if (monitor_interval_var.get() != 0):
                temp = "-m " + str(monitor_interval_var.get())
                para_list.append(temp)

            if (monitor_para_var.get()):
                temp = "-M " + monitor_para_var.get()
                para_list.append(temp)
            
            if (uti_var.get()):
                temp = "-u " + uti_var.get()
                para_list.append(temp)
            
            if (ver_var.get() != "ORG"):
                temp = "-e " + ver_var.get()
                para_list.append(temp)

            
            final_para = " ".join(para_list)



            return final_para


        run_frame = ctk.CTkFrame(self)
        run_frame.pack(expand=True, fill = 'both', padx= 300, pady = 20)




        def run_subprocess():
            para = format_parameters()

            command2 = ["python3", "cqsim.py"] + para.split()
            self.subprocess = subprocess.Popen(command2)
            self.subprocess.wait()

            controller.frames[RunningPage].done_button()


        def start_sim():
            controller.frames[RunningPage].start_button()
            # controller.frames[RunningPage].start_live_graph_animation()
            controller.show_frame(RunningPage)
            threading.Thread(target=controller.frames[RunningPage].start_live_graph_animation).start()
            
            # Start the subprocess in a separate thread
            subprocess_thread = threading.Thread(target=run_subprocess)
            subprocess_thread.start()



        run_button = ctk.CTkButton(run_frame, text = 'Run CQSim', font = ('Arial', 20), command = start_sim, fg_color='#20C6D6', text_color='black')
        run_button.pack(expand = True, fill = 'both')

# LIVE GRAPH ======================================================================================

class RunningPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg= '#FBFBFB')

        self.f = Figure(figsize=(5, 5), dpi=100)
        self.ax1 = self.f.add_subplot(1, 1, 1)
        self.ax1.clear()

        self.max_x = 500000
        self.xar = []
        self.yar = []

        self.job_name = tk.StringVar(value = None)
        label2 = tk.Label(self, textvariable=self.job_name, font = LARGE_FONT, background="#FBFBFB")
        label2.pack(pady=10,padx=10)

        # A Go Back Button that cancels the animation and simulation
        def go_back():
            self.controller.show_frame(StartPage)
            self.animation_running = False
            self.ani.event_source.stop() 

            self.controller.frames[StartPage].subprocess.terminate()

        self.back_button = ctk.CTkButton(self, text="Back", command= go_back, fg_color='#B6B6B6', text_color='black')
        self.back_button.pack(pady=10, padx=10)

        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)


        # Initialize the animation function as None
        self.ani = animation.FuncAnimation(self.f, self.animate, interval=1)
        self.stop_animation()

    # Starts the animation for the graph
    def start_animation(self):
        # Start the animation
        self.animation_running = True
        self.ani.event_source.start()

    # Stops the animation for the graph
    def stop_animation(self):
        # Stop the animation
        self.animation_running = False
        self.ani.event_source.stop()    

    # Makes the button blue when CQSim is done
    def done_button(self):
        self.back_button.configure(fg_color='#20C6D6')

    # Makes the button be grey when we start running CQSIM
    def start_button(self):
        self.back_button.configure(fg_color='#B6B6B6')

    # Clearing data and setting up the graph to look good
    def start_live_graph_animation(self):
        
        # Clear old data
        self.xar = []
        self.yar = []

        # Gets the current job name
        self.job_name.set(self.controller.frames[StartPage].job_name_var.get())

        # Clears the graphs
        if self.job_name.get():
            fileName = "../data/Results/" + str(self.job_name.get()) + ".ult"
        else:
            fileName = "../data/Results/SDSC-SP2-1998-4.ult"

        with open(fileName, 'w'):
            pass

        if self.job_name.get():
            fileName = "../data/Results/" + str(self.job_name.get()) + ".rst"
        else:
            fileName = "../data/Results/SDSC-SP2-1998-4.rst" # default

        with open(fileName, 'w'):
            pass

        # Resets variables for reading
        self.last_line = 0
        self.job_total = 0
        self.wait_total = 0
        self.max_wait = 0
        self.job_ids = []

        # Start the animation if it's not already running
        if not self.animation_running:
            self.start_animation()

        self.after(500, self.display_graph_page)

    def display_graph_page(self):
        # Code to display the graph page
        self.controller.show_frame(RunningPage) 

    # Graphing the utilization of the simulation
    def utilization_graph(self):
        if not self.animation_running:
            return  # Do nothing if animation is not running

        # System info log
        if self.job_name.get():
            fileName = "../data/Results/" + str(self.job_name.get()) + ".ult"
        else:
            fileName = "../data/Results/SDSC-SP2-1998-4.ult" # default

        # Check if last_line attribute exists, if not initialize it to 0
        if not hasattr(self, 'last_line'):
            self.last_line = 0

        # Empties file so the graph starts empty
        with open(fileName, 'r') as file:
            file.seek(self.last_line)
            pullData = file.read()
            self.last_line = file.tell()
            file.close()
        dataArray = pullData.split('\n')

        # Reads the file and puts the data into the array
        for eachline in dataArray:
            if (len(eachline) > 1):
                eventArray = eachline.split(';')
                if (eventArray[1] == 'E' or eventArray[1] == 'S'):
                    waitNum_index = eventArray[3].find(" waitNum=")

                    # Getting the util
                    uti_value = eventArray[3][4:waitNum_index]

                    self.xar.append(float(eventArray[2]))
                    self.yar.append(float(uti_value))


        # Calculate the maximum x-value dynamically
        max_x_value = max(self.xar) if self.xar else 0

        # Calculate the start index based on the maximum x-axis limit
        start_index = max(0, max_x_value - self.max_x)

        self.ax1.clear()
        self.ax1.step(self.xar, self.yar, where='post')
        self.ax1.margins(2, 2)
        self.ax1.set_xlim(start_index, start_index + self.max_x)
        self.ax1.set_ylim(-.1, 1.1)
        self.ax1.set_ylabel("Utilization")
        self.ax1.set_xlabel("Time")
        self.ax1.set_title("Utilization Graph")

        # Customize the x-axis tick marks
        x_ticks_multiple = 86400

        # Get the current x-axis
        ax = self.f.gca().xaxis

        # Set the tick locator to occur at multiples of x_ticks_multiple
        ax.set_major_locator(ticker.MultipleLocator(base=x_ticks_multiple))

        # Define the format for the tick labels
        day_label_format = "Day {:d}"

        # Create a custom formatter using a function
        def format_day_label(x, pos):
            day_value = int(x / x_ticks_multiple) + 1
            return day_label_format.format(day_value)

        # Set the tick label formatter for the x-axis
        ax.set_major_formatter(ticker.FuncFormatter(format_day_label))

        # Update the canvas with the new plot
        self.canvas.draw()

    def avg_wait_graph(self):
        if not self.animation_running:
            return  # Do nothing if animation is not running

        # System info log
        if self.job_name.get():
            fileName = "../data/Results/" + str(self.job_name.get()) + ".rst"
        else:
            fileName = "../data/Results/SDSC-SP2-1998-4.rst" # default

        # Check if last_line attribute exists, if not initialize it to 0
        if not hasattr(self, 'last_line'):
            self.last_line = 0

        # Empties file so the graph starts empty
        with open(fileName, 'r') as file:
            file.seek(self.last_line)
            pullData = file.read()
            self.last_line = file.tell()
            file.close()
        dataArray = pullData.split('\n')

        # Reads the file and puts the data into the array
        for eachline in dataArray:
            if (len(eachline) > 1):
                self.job_total = self.job_total + 1

                eventArray = eachline.split(';')
                
                wait_time = float(eventArray[5])

                self.wait_total = self.wait_total + wait_time

                avg = self.wait_total / self.job_total


                self.xar.append(float(eventArray[8]))
                self.yar.append(avg)


        # Calculate the maximum x-value dynamically
        max_x_value = max(self.xar) if self.xar else 0

        # Calculate the start index based on the maximum x-axis limit
        start_index = max(0, max_x_value - self.max_x)

        self.ax1.clear()
        self.ax1.plot(self.xar, self.yar)
        self.ax1.margins(2, 2)
        self.ax1.set_xlim(start_index, start_index + self.max_x)
        self.ax1.set_ylim(bottom=-1)

        # Set a custom maximum value for the y-axis to create a smaller margin
        if (len(self.yar) > 1):
            if (len(self.yar) > 1000):
                max_y_value = max(self.yar[-1000:]) * 1.35
            else:
                max_y_value = max(self.yar) * 1.15  # You can adjust the factor (e.g., 1.05) to control the margin
        else:
            max_y_value = 1000
        self.ax1.set_ylim(top=max_y_value)

        self.ax1.set_ylabel("Job Wait Time")
        self.ax1.set_xlabel("Time")
        self.ax1.set_title("Average Job Wait Time")

        # Customize the x-axis tick marks
        x_ticks_multiple = 86400

        # Get the current x-axis
        ax = self.f.gca().xaxis

        # Set the tick locator to occur at multiples of x_ticks_multiple
        ax.set_major_locator(ticker.MultipleLocator(base=x_ticks_multiple))

        # Define the format for the tick labels
        day_label_format = "Day {:d}"

        # Create a custom formatter using a function
        def format_day_label(x, pos):
            day_value = int(x / x_ticks_multiple) + 1
            return day_label_format.format(day_value)

        # Set the tick label formatter for the x-axis
        ax.set_major_formatter(ticker.FuncFormatter(format_day_label))

        # Legend to show the avg as of this moment
        if (len(self.yar) > 1):
            self.ax1.legend([f"Average Wait Time: {self.yar[-1]:.2f})"])

        # Update the canvas with the new plot
        self.canvas.draw()

    def max_wait_graph(self):
        if not self.animation_running:
            return  # Do nothing if animation is not running

        # System info log
        if self.job_name.get():
            fileName = "../data/Results/" + str(self.job_name.get()) + ".rst"
        else:
            fileName = "../data/Results/SDSC-SP2-1998-4.rst" # default

        # Check if last_line attribute exists, if not initialize it to 0
        if not hasattr(self, 'last_line'):
            self.last_line = 0

        # Empties file so the graph starts empty
        with open(fileName, 'r') as file:
            file.seek(self.last_line)
            pullData = file.read()
            self.last_line = file.tell()
            file.close()
        dataArray = pullData.split('\n')

        # Reads the file and puts the data into the array
        for eachline in dataArray:
            if (len(eachline) > 1):

                eventArray = eachline.split(';')
                
                wait_time = float(eventArray[5])
                job_id = int(eventArray[0])

                # Sets the data to the max 
                if (wait_time > self.max_wait):
                    self.job_total = self.job_total + 1
                    self.max_wait = wait_time
                    self.job_ids.append(job_id)

                    self.xar.append(self.job_total)
                    self.yar.append(wait_time)
                else:
                    wait_time = self.max_wait


        # Calculate the maximum x-value dynamically
        max_x_value = max(self.xar) if self.xar else 0

        # Calculate the start index based on the maximum x-axis limit
        start_index = max(0, max_x_value - 10)

        self.ax1.clear()
        self.ax1.plot(self.xar, self.yar)
        self.ax1.plot(self.xar, self.yar, marker='o', linestyle='-', color='b', label='Max Wait Time')
        # self.ax1.plot(self.xar, self.yar)

        self.ax1.set_xlim(start_index, start_index + 10)
        self.ax1.set_ylim(bottom=-1)

        # Set a custom maximum value for the y-axis to create a smaller margin
        if len(self.yar) > 1:
            max_y_value = max(self.yar) * 1.15 
        else:
            max_y_value = 1000
        self.ax1.set_ylim(top=max_y_value)

        # Text on graphs
        self.ax1.set_ylabel("Job Wait Time")
        self.ax1.set_xlabel("Job ID")
        self.ax1.set_title("Max Job Wait Time")

        self.ax1.xaxis.set_major_locator(ticker.FixedLocator(self.xar))
        self.ax1.xaxis.set_major_formatter(ticker.FixedFormatter(self.job_ids))
        self.ax1.set_xticklabels(self.ax1.get_xticklabels(), rotation=45, ha='right')
        
        # Update the canvas with the new plot
        self.canvas.draw()

    # Animate func
    def animate(self, i):
        graph_num = int(self.controller.frames[StartPage].graph_var.get())

        if (graph_num == 0): # Utilization
            self.utilization_graph()
        elif (graph_num == 1): # MAX Job Wait
            self.max_wait_graph()
        elif (graph_num == 2): # Avg Job Wait
            self.avg_wait_graph()
        else:
            print("ERROR WITH THE CHECKBOXES")


       

app = CQSimGUI()
app.mainloop()