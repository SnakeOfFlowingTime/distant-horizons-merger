import sqlite3
import json

with open("config.json", "r") as config:
    configs = json.load(config)

primary = configs["primary"]
secondary = configs["secondary"]

print("Connecting To Primary DB...")
conn = sqlite3.connect(primary)
print("Connected.")
cursor = conn.cursor()

cursor.execute(f"ATTACH DATABASE '{secondary}' AS secondary;")
print("Attached Secondary DB.")
cursor.execute(f"SELECT name FROM secondary.sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

print("Merging...")
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