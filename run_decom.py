# loadmat is used to load MATLAB data

import warnings
from scipy.stats._stats_py import SmallSampleWarning
import os

os.environ["LOKY_MAX_CPU_COUNT"] = "8"

warnings.filterwarnings("ignore", category=SmallSampleWarning)
from scipy.io import loadmat

# Pickle allows saving and loading Python objects into a file
import os
# from logger import setup_experiment_logger, print
import scipy.io as sio
import pickle as pkl
import joblib as jb


from emgdecompy.decomposition import *
from emgdecompy.contrast import *
from emgdecompy.viz import *
from emgdecompy.preprocessing import *
from file_utils import find_mat_files, load_mat_file, update_mat_file, save_pkl_file
import argparse 

import tkinter as tk
from tkinter import filedialog

import traceback


def find_mat_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    else:
        mat_files = [f for f in os.listdir(directory) if f.endswith('.mat')]
        # print(mat_files)
        # sorted_mat_files = sorted(mat_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        return mat_files

def find_pkl_files(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory {directory} does not exist.")
    else:
        pkl_files = [f for f in os.listdir(directory) if f.endswith(('.pkl', '.pickle'))]
        try:
            # Try to sort by number in filename
            sorted_pkl_files = sorted(pkl_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        except (ValueError, IndexError):
            # If sorting by number fails, sort alphabetically
            sorted_pkl_files = sorted(pkl_files)
        return pkl_files, sorted_pkl_files

    
def load_mat_file(file_path):
    data = sio.loadmat(file_path)
    return data

def update_mat_file(data, file_dir, file_name):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        print(f"Created directory: {file_dir}")
    
    else:
        file_path = os.path.join(file_dir, file_name)
        sio.savemat(file_path, data)
    print(f"Updated file: {file_path}")

def save_pkl_file(data, file_dir, file_name):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        print(f"Created directory: {file_dir}")
    file_path = os.path.join(file_dir, file_name)
    jb.dump(data, file_path)
    print(f"Updated file: {file_path}")

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

def select_single_pkl_file(pkl_files):
    def on_select():
        selected_indices = listbox.curselection()
        if selected_indices:  # Check if any selection was made
            selected_file = listbox.get(selected_indices[0])  # Get only the first selection
            window.selected_file = selected_file
        window.quit()
        window.destroy()

    window = tk.Tk()
    window.title("Select PKL file")
    window.selected_file = None
    
    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)
    
    label = tk.Label(frame, text="Select a single pkl file")
    label.pack()
    
    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=50)  # Changed to SINGLE mode
    listbox.pack()
    
    for file in pkl_files:
        listbox.insert(tk.END, file)
    
    select_button = tk.Button(frame, text="Select", command=on_select)
    select_button.pack(pady=10)
    
    window.mainloop()
    return window.selected_file

def select_single_mat_file(pkl_files):
    def on_select():
        selected_indices = listbox.curselection()
        if selected_indices:  # Check if any selection was made
            selected_file = listbox.get(selected_indices[0])  # Get only the first selection
            window.selected_file = selected_file
        window.quit()
        window.destroy()

    window = tk.Tk()
    window.title("Select PKL file")
    window.selected_file = None
    
    frame = tk.Frame(window)
    frame.pack(padx=10, pady=10)
    
    label = tk.Label(frame, text="Select a single mat file")
    label.pack()
    
    listbox = tk.Listbox(frame, selectmode=tk.SINGLE, width=50)  # Changed to SINGLE mode
    listbox.pack()
    
    for file in pkl_files:
        listbox.insert(tk.END, file)
    
    select_button = tk.Button(frame, text="Select", command=on_select)
    select_button.pack(pady=10)
    
    window.mainloop()
    return window.selected_file

def select_path(message:str="Select folder for raw data"):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=message)
    return folder_path

def visualize_result():
    import panel as pn
    import sys
    
    # Initialize panel extension for running outside notebook
    pn.extension()
    
    def close_app(event):
        """Close the application and exit"""
        sys.exit(0)
    
    result_dir = select_path("Please select directory for result files")
    mat_files = find_mat_files(result_dir)
    selected_file = select_single_mat_file(mat_files)
    data = load_mat_file(os.path.join(result_dir, selected_file))
    raw = data["SIG"]
    name = selected_file[:-4]
    pkl_file = f"{name}_decom.pkl"
    output = jb.load(os.path.join(result_dir, pkl_file))
    
    # Create the dashboard
    dashboard = visualize_decomp(output, raw)
    
    # Add a close button
    close_button = pn.widgets.Button(name='Close Visualization', button_type='danger')
    close_button.on_click(close_app)
    
    # Add the close button to the dashboard
    dashboard_with_button = pn.Column(dashboard, close_button)
    
    # Serve the panel application
    dashboard_with_button.show(title=f"Decomposition Results - {name}", port=5006)

def select_action():
    """
    Create a GUI window to select multiple actions to perform using checkboxes
    
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

    window = tk.Tk()
    window.title("Select Actions")
    window.selected_actions = []
    
    frame = tk.Frame(window)
    frame.pack(padx=20, pady=20)
    
    label = tk.Label(frame, text="Select one or more actions:", font=('Arial', 12))
    label.pack(pady=10)
    
    # Create variables for checkboxes
    decompose_var = tk.BooleanVar()
    plot_var = tk.BooleanVar()
    save_var = tk.BooleanVar()
    
    # Create checkboxes
    decompose_check = tk.Checkbutton(frame, text="Decompose", variable=decompose_var, font=('Arial', 10))
    decompose_check.pack(pady=5, anchor='w')
    
    plot_check = tk.Checkbutton(frame, text="Plot", variable=plot_var, font=('Arial', 10))
    plot_check.pack(pady=5, anchor='w')
    
    save_check = tk.Checkbutton(frame, text="Save", variable=save_var, font=('Arial', 10))
    save_check.pack(pady=5, anchor='w')
    
    # Create buttons frame
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=15)
    
    confirm_button = tk.Button(button_frame, text="Confirm", command=on_confirm, width=10)
    confirm_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel, width=10)
    cancel_button.pack(side=tk.LEFT, padx=5)
    
    # Center the window on the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    window.mainloop()
    return window.selected_actions

def main():

    """
    Run the motor unit decomposition pipeline
    """
    def select_folder(message:str="Select folder for raw data"):
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title=message)
        return folder_path
    try:
        # log_dir = select_folder("Please select directory for log files")
        # print(f"Selected folder: {log_dir}, all log files will be saved in this directory")
        # logger = setup_experiment_logger(name="mudecomp", report_dir=log_dir)
        # print( f"Selected folder: {log_dir}, all log files will be saved in this directory")

        data_dir = select_folder("Please select directory for raw data")
        print( f"Selected folder: {data_dir} for raw data")

        mat_files = find_mat_files(data_dir)

        selected_files = select_files_from_list(mat_files)
        print( f"Selected files: {selected_files}")

        output_dir = select_folder("Please select directory for output data")

        for file in selected_files:
            print( f"Processing file: {file}")
            
            file_name = os.path.join(data_dir, file)
            name = file[:-4]
            # data = load_mat_file(file_name)
            # raw = data["SIG"]
            # discard_channel = data["discardChannelsVec"]
            # fsamp = data["fsamp"]
            # print( f"Sampling rate: {fsamp}")
            # iterations = data["DecompRuns"]
            # print( f"Will run decomposition for {iterations[0][0]} iterations")
            # threshold = True
            # if threshold == False:
            #     PNR_list = data["PNR"]
            #     min_pnr = min(PNR_list)
            #     print( f"Minimum PNR: {min_pnr}")
            #     pnr_thred = float(input("Enter PNR threshold: "))
            #     thred = pnr_thred
            # else:
            #     thred = 0.9
            data = loadmat(file_name)
            raw = data['SIG']
            discard =data["discardChannelsVec"]
            fsamp = data["fsamp"]
            iterations = data["DecompRuns"]
            flatten = flatten_signal(discard)
            discard = np.where(flatten==1)
            arr = discard[0]
            discard_edited = arr[arr != 0] - 1
            discard = (discard_edited,)
            print(f"Discard channels: {discard_edited}")

            output = decomposition(
                raw,
                discard=discard,
                R=16,
                M=150,
                bandpass=True,
                lowcut=10,
                highcut=900,
                fs=2048,
                order=6,
                Tolx=10e-4,
                contrast_fun=skew,
                ortho_fun=gram_schmidt,
                max_iter_sep=10,
                l=31,
                sil_pnr=True,
                thresh=0.9,
                max_iter_ref=20,
                random_seed=None,
                verbose=True
            )
            MuPulse = output["MUPulses"]
            MuPulse_reshaped = [arr.reshape(1, -1) for arr in MuPulse]
            MuPulse_cell = np.zeros((1, len(MuPulse_reshaped)), dtype=object)
            for i, arr in enumerate(MuPulse_reshaped):
                arr = arr.astype(np.float64)
                MuPulse_cell[0, i] = arr
            MuPulse = MuPulse_cell
            old_MuPulse = data["MUPulses"]
            B = output["B"]
            print(f"The shape of B is {B.shape}")
            data["Sep_Vec"] = B
            data["old_MUPulses"] = old_MuPulse
            data["MUPulses"] = MuPulse
            print(f"The shape of MUPulses is {MuPulse.shape}")
            old_pnr = data["PNR"]
            num_mus = output["IPTs"].shape[0]
            MUID = [f"A{i}" for i in range(1, num_mus+1)]
            MUIDs = np.array(MUID, dtype=object)
            data["old_MUIDs"] = data["MUIDs"]
            data["MUIDs"] = MUIDs
            data["old_PNR"] = old_pnr
            data["PNR"] = output["PNR"]
            print(f"The new PNR is {output['PNR']}")
            data["SIL"] = output["SIL"]
            old_ipts = data["IPTs"]
            data["old_IPTs"] = old_ipts
            data["IPTs"] = output["IPTs"]
            print(f"The new SIL is {output['SIL']}")
            update_mat_fname = f"{name}_I150_EmgDecomPy.mat"
            update_mat_file(data, output_dir, update_mat_fname)
            output_name = f"{name}_I150_decom.pkl"
            save_pkl_file(output, output_dir, output_name)

            # visualize = input("Visualize result? (y/n)")
            # if visualize == "y":
            #     visualize_result()
            # else:
            #     print("Skipping visualization")
        
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}")
        print(f"End with error: {e}")


        



if __name__ == "__main__":
    selected_actions = select_action()
    if not selected_actions:
        print("Operation cancelled")
    else:
        if 'decompose' in selected_actions:
            main()
        if 'plot' in selected_actions:
            visualize_result()
        if 'save' in selected_actions:
            # Add save functionality here if needed
            print("Save functionality not implemented yet")
