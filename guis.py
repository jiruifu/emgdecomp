import tkinter as tk
from tkinter import filedialog
import os
def select_folder(message:str="Select folder for raw data"):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=message)
    return folder_path

def find_mat_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    else:
        mat_files = [f for f in os.listdir(directory) if f.endswith('.mat')]
        # print(mat_files)
        # sorted_mat_files = sorted(mat_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        return mat_files

def select_files_from_list(mat_files):
    """
    Create a GUI window to select .mat files from a list
    
    Args:
        mat_files (list): List of available .mat files
        
    Returns:
        list: Selected .mat files
    """
    def on_select():
        selected_indices = listbox.curselection()
        selected_files = [listbox.get(i) for i in selected_indices]
        window.selected_files = selected_files
        window.quit()  # First quit the mainloop
        window.destroy()  # Then destroy the window

    window = tk.Tk()
    window.title("Select .mat files")
    window.selected_files = []
    
    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)
    
    label = tk.Label(frame, text="Select one or multiple .mat files (hold Ctrl/Cmd for multiple)")
    label.pack()
    
    listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=50)
    listbox.pack()
    
    for file in mat_files:
        listbox.insert(tk.END, file)
    
    select_button = tk.Button(frame, text="Select", command=on_select)
    select_button.pack(pady=10)
    
    window.mainloop()
    return window.selected_files

def select_action():
    """
    Create a GUI window to select multiple actions to perform using toggle switches
    
    Returns:
        list: List of selected actions ('decompose', 'plot', 'save')
    """
    def on_confirm():
        selected_actions = []
        if decompose_var.get():
            selected_actions.append('decompose')
        if plot_var.get():
            selected_actions.append('plot')
        if save_var.get():
            selected_actions.append('save')
        window.selected_actions = selected_actions
        window.quit()
        window.destroy()
        
    def on_cancel():
        window.selected_actions = []
        window.quit()
        window.destroy()

    class ToggleSwitch(tk.Canvas):
        def __init__(self, parent, variable, width=100, height=50, *args, **kwargs):
            super().__init__(parent, width=width, height=height, *args, **kwargs)
            self.width = width
            self.height = height
            self.variable = variable
            self.state = variable.get()
            
            # Colors
            self.bg_color = '#f0f0f0'
            self.off_color = '#e74c3c'
            self.on_color = '#2ecc71'
            self.knob_color = '#ffffff'
            
            # Create the switch
            self.configure(bg=self.bg_color, highlightthickness=0)
            self.create_switch()
            
            # Bind click event
            self.bind('<Button-1>', self.toggle)
            
        def create_switch(self):
            # Create the background track
            self.track = self.create_rectangle(
                5, 5, self.width-5, self.height-5,
                fill=self.on_color if self.state else self.off_color,
                outline='',
                width=0
            )
            
            # Create the knob
            knob_size = self.height - 10
            x_pos = self.width - knob_size - 5 if self.state else 5
            self.knob = self.create_oval(
                x_pos, 5, x_pos + knob_size, knob_size + 5,
                fill=self.knob_color,
                outline='',
                width=0
            )
            
        def toggle(self, event=None):
            self.state = not self.state
            self.variable.set(self.state)  # Update the variable
            self.animate_switch()
            
        def animate_switch(self):
            # Update track color
            self.itemconfig(self.track, fill=self.on_color if self.state else self.off_color)
            
            # Calculate new knob position
            if self.state:
                new_x = self.width - self.height + 5
            else:
                new_x = 5
                
            # Animate knob movement
            current_x = self.coords(self.knob)[0]
            steps = 10
            step_size = (new_x - current_x) / steps
            
            def move_step(step=0):
                if step < steps:
                    self.move(self.knob, step_size, 0)
                    self.after(10, lambda: move_step(step + 1))
            
            move_step()
            
        def get(self):
            return self.state
            
        def set(self, value):
            if self.state != value:
                self.state = value
                self.variable.set(value)
                self.animate_switch()

    # Create and configure the main window
    window = tk.Tk()
    window.title("EMG Decomposition Tool")
    window.selected_actions = []
    
    # Set window background color
    window.configure(bg='#f0f0f0')
    
    # Create main frame with padding and background
    main_frame = tk.Frame(window, bg='#f0f0f0', padx=30, pady=30)
    main_frame.pack(expand=True, fill='both')
    
    # Title label with custom font and color
    title_label = tk.Label(
        main_frame,
        text="Select Actions",
        font=('Helvetica', 16, 'bold'),
        bg='#f0f0f0',
        fg='#2c3e50'
    )
    title_label.pack(pady=(0, 20))
    
    # Subtitle label
    subtitle_label = tk.Label(
        main_frame,
        text="Toggle switches to select actions:",
        font=('Helvetica', 10),
        bg='#f0f0f0',
        fg='#34495e'
    )
    subtitle_label.pack(pady=(0, 15))
    
    # Create a frame for toggle switches
    switch_frame = tk.Frame(main_frame, bg='#f0f0f0')
    switch_frame.pack(pady=10)
    
    # Create variables for switches
    decompose_var = tk.BooleanVar(value=False)
    plot_var = tk.BooleanVar(value=False)
    save_var = tk.BooleanVar(value=False)
    
    # Style configuration for labels
    label_style = {
        'font': ('Helvetica', 12, 'bold'),
        'bg': '#f0f0f0',
        'fg': '#2c3e50',
        'padx': 15,
        'pady': 10
    }
    
    # Create toggle switches with labels
    def create_switch_row(parent, text, variable):
        frame = tk.Frame(parent, bg='#f0f0f0')
        frame.pack(pady=15)
        
        label = tk.Label(frame, text=text, **label_style)
        label.pack(side=tk.LEFT, padx=(0, 20))
        
        switch = ToggleSwitch(frame, variable, width=120, height=60)
        switch.pack(side=tk.LEFT)
        
        return frame
    
    # Create switch rows
    create_switch_row(switch_frame, "Decompose", decompose_var)
    create_switch_row(switch_frame, "Plot", plot_var)
    create_switch_row(switch_frame, "Save", save_var)
    
    # Create buttons frame with custom styling
    button_frame = tk.Frame(main_frame, bg='#f0f0f0')
    button_frame.pack(pady=20)
    
    # Button style configuration
    button_style = {
        'font': ('Helvetica', 10, 'bold'),
        'width': 12,
        'borderwidth': 0,
        'padx': 15,
        'pady': 8
    }
    
    # Create styled buttons
    confirm_button = tk.Button(
        button_frame,
        text="Confirm",
        command=on_confirm,
        bg='#2ecc71',
        fg='white',
        activebackground='#27ae60',
        activeforeground='white',
        **button_style
    )
    confirm_button.pack(side=tk.LEFT, padx=10)
    
    cancel_button = tk.Button(
        button_frame,
        text="Cancel",
        command=on_cancel,
        bg='#e74c3c',
        fg='white',
        activebackground='#c0392b',
        activeforeground='white',
        **button_style
    )
    cancel_button.pack(side=tk.LEFT, padx=10)
    
    # Add hover effects
    def on_enter(e):
        e.widget['background'] = '#27ae60' if e.widget == confirm_button else '#c0392b'
    
    def on_leave(e):
        e.widget['background'] = '#2ecc71' if e.widget == confirm_button else '#e74c3c'
    
    confirm_button.bind("<Enter>", on_enter)
    confirm_button.bind("<Leave>", on_leave)
    cancel_button.bind("<Enter>", on_enter)
    cancel_button.bind("<Leave>", on_leave)
    
    # Center the window on the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    # Make window resizable
    window.resizable(False, False)
    
    window.mainloop()
    return window.selected_actions

if __name__ == "__main__":
    # test the select_action function
    actions = select_action()
    print(actions)
    # check is decompose is in the list
    if len(actions) > 0:
        if "decompose" in actions:
            print("Decompose is in the list")
        else:
            print("Decompose is not in the list")
    else:
        print("No actions selected")
