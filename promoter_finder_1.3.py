import tkinter as tk
from tkinter import filedialog
import re

def find_variable_motif(sequence, motif, max_mismatches):
    positions = []
    motif_pattern = re.compile(re.escape(motif).replace('X', '[ATCG]'))  # Replace 'X' with '[ATCG]'
    motif_len = len(motif)

    for i in range(len(sequence) - motif_len + 1):
        subsequence = sequence[i:i + motif_len]

        # Count mismatches and consider 'X' as a wildcard character
        mismatch_count = sum(1 for a, b in zip(subsequence, motif) if a != b and b != 'X')

        if mismatch_count <= max_mismatches:
            positions.append(i)

    return positions

def clear_input_boxes():
    # Clear all input boxes
    fasta_entry.delete(0, tk.END)
    motif_entry.delete(0, tk.END)
    mismatches_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)

def read_fasta(file_path):
    with open(file_path, 'r') as fasta_file:
        lines = fasta_file.readlines()
        sequence = ''.join([line.strip() for line in lines[1:]])  # Skip the first line (header)

    return sequence

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        fasta_entry.delete(0, tk.END)
        fasta_entry.insert(0, file_path)

def search_motif():
    motif = motif_entry.get()
    max_mismatches = int(mismatches_entry.get())
    fasta_file_path = fasta_entry.get()

    sequence = read_fasta(fasta_file_path)

    positions = find_variable_motif(sequence, motif, max_mismatches)

    if positions:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Number of sites found: {len(positions)}\n")
        for pos in positions:
            result_text.insert(tk.END, f"Position: {pos}\n")
        result_text.config(fg='#21BF73')
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"The motif '{motif}' with up to {max_mismatches} mismatches was not found in the sequence.")
        result_text.config(fg='#FD5E53')

# Create the main window
window = tk.Tk()
window.title("Promoter Finder")
window.configure(bg='#FAEEE7')  # Set background color

# Create and configure GUI elements
frame = tk.Frame(window, bg='#FAEEE7')  # Set background color of the frame
frame.pack()

# Add instructions label
instructions_label = tk.Label(frame, text="Instructions:\n1. Manually enter a sequence in FASTA format or click 'Browse' to select a FASTA file.\n2. Enter the motif to search for and set a number of maximum mismatches allowed.\n3. Click 'Search Motif' to find the motif in the sequence. \n4 To insert a wildcard character in the motif insert the letter X in the desired position.", bg='#FAEEE7', fg='#325288', font=("Arial", 11))
instructions_label.pack()

tk.Label(frame, text="Fasta File:", bg='#FAEEE7', fg='#325288').pack()
fasta_entry = tk.Entry(frame, width=50)
fasta_entry.pack()
browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.pack()

tk.Label(frame, text="Motif:", bg='#FAEEE7', fg='#325288').pack()
motif_entry = tk.Entry(frame, width=50)
motif_entry.pack()

tk.Label(frame, text="Max Mismatches:", bg='#FAEEE7', fg='#325288').pack()
mismatches_entry = tk.Entry(frame, width=50)
mismatches_entry.pack()

search_button = tk.Button(frame, text="Search Motif", command=search_motif)
search_button.pack()

reset_button = tk.Button(frame, text="Reset", command=clear_input_boxes)
reset_button.pack()

result_text = tk.Text(frame, wrap="word", width=50, height=10)
result_text.pack()

# Start the GUI event loop
window.mainloop()
