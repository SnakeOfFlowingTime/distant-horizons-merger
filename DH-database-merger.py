import sqlite3
import tkinter as tk
from tkinter import filedialog

def databaseMerger(primary, secondary):
    print("Connecting To Primary DB...")
    submit_button.config(text="Connecting To Primary DB.")
    conn = sqlite3.connect(primary)
    print("Connected.")
    submit_button.config(text="Connected.")
    cursor = conn.cursor()

    cursor.execute(f"ATTACH DATABASE '{secondary}' AS secondary;")
    print("Attached Secondary DB.")
    submit_button.config(text="Attached Secondary DB.")
    cursor.execute(f"SELECT name FROM secondary.sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    print("Merging...")
    submit_button.config(text="Merging...")
    for table in tables:
        cursor.execute(f"PRAGMA secondary.table_info({table});")
        columns = [row[1] for row in cursor.fetchall()]
    
        column_list = ", ".join(columns)
    
        cursor.execute(f"""
            INSERT OR IGNORE INTO main.{table} ({column_list}) 
            SELECT {column_list} FROM secondary.{table};
        """)

    conn.commit()
    print("Done.")
    conn.close()
    submit_button.config(text="Done.")

root = tk.Tk()

root.title("Distant Horizons SQLite Merger")

root.geometry("512x512")

main_file_path = filedialog.askopenfilename(
    title="Select Main File, The One Who Will Receive The Data",
    filetypes=(("SQLite Database", "*.sqlite"),)
)

secondary_file_path = filedialog.askopenfilename(
    title="Select Secondary File, The One Who Will Send The Data",
    filetypes=(("SQLite Database", "*.sqlite"),)
)

main_label = tk.Label(root, text="Main:")
main_label.grid(row=0, column=0, padx=16, pady=16, sticky="e")

main_entry = tk.Entry(root, width=64)
main_entry.grid(row=0, column=1, padx=16, pady=16)
main_entry.insert(0, f"{main_file_path}")

secondary_label = tk.Label(root, text="Secondary:")
secondary_label.grid(row=1, column=0, padx=16, pady=16, sticky="e")

secondary_entry = tk.Entry(root, width=64)
secondary_entry.grid(row=1, column=1, padx=16, pady=16)
secondary_entry.insert(0, f"{secondary_file_path}")

submit_button = tk.Button(root, text="Merge", command=lambda: databaseMerger(main_file_path, secondary_file_path))
submit_button.grid(row=2, column=0, columnspan=16, pady=16)

root.mainloop()

