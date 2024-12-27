import os
import PyPDF2
from tkinter import Tk, Label, Entry, Button, filedialog, Listbox, Scrollbar, END

def browse_folder():
    """Open a dialog to select a folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, END)
        folder_entry.insert(0, folder_path)

def search_files():
    """Search for PDFs containing the search term in their content."""
    folder = folder_entry.get()
    search_term = search_entry.get()

    if not folder or not os.path.isdir(folder):
        result_listbox.insert(END, "Please select a valid folder.")
        return

    if not search_term:
        result_listbox.insert(END, "Please enter a search term.")
        return

    result_listbox.delete(0, END)  # Clear previous results

    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                if search_pdf(file_path, search_term):
                    result_listbox.insert(END, file_path)

def search_pdf(file_path, search_term):
    """Check if the search term exists in the PDF content."""
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                if text and search_term.lower() in text.lower():
                    return True
    except Exception as e:
        result_listbox.insert(END, f"Error reading {file_path}: {e}")
    return False

def open_file():
    """Open the selected file from the result list."""
    selected = result_listbox.curselection()
    if selected:
        file_path = result_listbox.get(selected[0])
        os.startfile(file_path)

# Initialize the GUI
root = Tk()
root.title("Certificate Search Tool")
root.geometry("600x400")

# Folder selection
Label(root, text="Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
folder_entry = Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=10, pady=5)
Button(root, text="Browse", command=browse_folder).grid(row=0, column=2, padx=10, pady=5)

# Search term input
Label(root, text="Search Term:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
search_entry = Entry(root, width=50)
search_entry.grid(row=1, column=1, padx=10, pady=5)

# Search button
Button(root, text="Search", command=search_files).grid(row=1, column=2, padx=10, pady=5)

# Result listbox with scrollbar
result_listbox = Listbox(root, width=70, height=15)
result_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

scrollbar = Scrollbar(root, command=result_listbox.yview)
scrollbar.grid(row=2, column=2, sticky="ns")
result_listbox.config(yscrollcommand=scrollbar.set)

# Open file button
Button(root, text="Open File", command=open_file).grid(row=3, column=1, pady=10)

# Run the GUI
root.mainloop()
