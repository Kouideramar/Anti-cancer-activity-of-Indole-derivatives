# Import necessary libraries
import os
import sys
import joblib
import numpy as np
from tkinter import Tk, Label, Entry, Button, Canvas, Frame, Scrollbar, messagebox

# Define resource path function for dynamic path resolution
def resource_path(relative_path):
    """Get the absolute path to the resource"""
    try:
        base_path = sys._MEIPASS  # Path for PyInstaller
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))  # Script directory
    return os.path.join(base_path, relative_path)

# Load model and scaler
try:
    model_path = resource_path('adb_model.pkl')  # Ensure the model is in the same directory
    scaler_path = resource_path('scaler.pkl')
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit("Model or scaler file not found. Ensure they are in the same directory as the script.")

# Define the required fields
fields = [
    'GATS1e', 'nS', 'MAXDP', 'nX', 'ETA_dBeta', 'GATS8p', 'GATS2s', 'PubchemFP213',
    'IC2', 'PubchemFP638', 'SIC5', 'PubchemFP335', 'AATS1i', 'AATS2i', 'VE1_Dzp',
    'SHBint3', 'VE1_Dzi', 'VE3_Dzi', 'AATS7s', 'nAtomP', 'PubchemFP375', 'BCUTc-1l',
    'BCUTc-1h', 'nBondsM', 'SdssC', 'SssNH', 'MLFER_BH', 'MPC8', 'PubchemFP716',
    'PubchemFP421', 'SpMin1_Bhv', 'piPC10', 'AATSC3v', 'n6HeteroRing', 'mindssC',
    'MATS2c', 'SpMin3_Bhi', 'JGT', 'TopoPSA', 'PubchemFP517', 'GATS3m', 'PubchemFP540',
    'PubchemFP16', 'GATS4c', 'hmax'
]

# Function to handle user input and predict IC50
def predict_ic50():
    """Collect user inputs, scale them using the loaded scaler, and predict IC50."""
    try:
        # Collect inputs from entry fields
        inputs = []
        for field in fields:
            value = entries[field].get()
            if value.strip() == "":
                raise ValueError(f"Missing value for {field}")
            inputs.append(float(value))
        
        # Scale inputs using the loaded scaler
        input_array = np.array(inputs).reshape(1, -1)
        input_scaled = scaler.transform(input_array)  # Use the loaded scaler for scaling
        
        # Predict IC50
        log_ic50 = model.predict(input_scaled)
        ic50 = 10**(log_ic50)  # Reverse log-transform

        # Display the result in a new pop-up
        messagebox.showinfo("Prediction Result", f"Predicted IC50: {ic50[0]:.4f} µM")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Create the main window
root = Tk()
root.title("IC50 Prediction")
root.geometry("800x500")  # Increased window dimensions

# Create a canvas for scrolling
canvas = Canvas(root)
scroll_y = Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_x = Scrollbar(root, orient="horizontal", command=canvas.xview)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")

# Create a frame inside the canvas
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
canvas.pack(side="left", fill="both", expand=True)

# Instructions
Label(frame, text="Enter the following molecular descriptors:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=8, pady=10)

# Create entry fields in a grid layout (4 columns)
entries = {}
row_num = 1
col_num = 0
for i, field in enumerate(fields):
    Label(frame, text=field, width=15, anchor="w").grid(row=row_num, column=col_num, padx=5, pady=5)
    entry = Entry(frame, width=10)
    entry.grid(row=row_num, column=col_num + 1, padx=5, pady=5)
    entries[field] = entry

    # Move to the next row after every 4 columns
    col_num += 2
    if col_num >= 8:
        col_num = 0
        row_num += 1

# Add a button to predict IC50
Button(frame, text="Predict IC50 of Indole derivatives", command=predict_ic50, bg="lightblue", fg="black").grid(row=row_num + 1, column=0, columnspan=8, pady=20)

# Configure the scrolling area
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Run the GUI
root.mainloop()
