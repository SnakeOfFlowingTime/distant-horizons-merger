import sqlite3
import tkinter as tk
from tkinter import filedialog

def databaseMerger(primary, secondary):
    print("Connecting To Primary DB...")
    submit_button.config(text="Connecting To Primary DB...")
    try: 
        conn = sqlite3.connect(primary)
    except:
        print("Something Went Wrong, Check if Main File is Correct.")
        submit_button.config(text="Error.")
        return
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
    try:
        for table in tables:
            cursor.execute(f"PRAGMA secondary.table_info({table});")
            columns = [row[1] for row in cursor.fetchall()]
    
            column_list = ", ".join(columns)
    
            cursor.execute(f"""
                INSERT OR IGNORE INTO main.{table} ({column_list}) 
                SELECT {column_list} FROM secondary.{table};
            """)
    except:
        print("Something Went Wrong, Check if Both Files are Correct.")
        submit_button.config(text="Error.")
        return 

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

main_text_variable= tk.StringVar()
main_entry = tk.Entry(root, width=64, textvariable=main_text_variable)
main_entry.grid(row=0, column=1, padx=16, pady=16)
main_entry.insert(0, f"{main_file_path}")

secondary_label = tk.Label(root, text="Secondary:")
secondary_label.grid(row=1, column=0, padx=16, pady=16, sticky="e")

secondary_text_variable= tk.StringVar()
secondary_entry = tk.Entry(root, width=64, textvariable=secondary_text_variable)
secondary_entry.grid(row=1, column=1, padx=16, pady=16)
secondary_entry.insert(0, f"{secondary_file_path}")

submit_button = tk.Button(root, text="Merge", command=lambda: databaseMerger(main_text_variable.get(), secondary_text_variable.get()))
submit_button.grid(row=2, column=0, columnspan=16, pady=16)

root.mainloop()

