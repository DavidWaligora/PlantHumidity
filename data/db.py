import sqlite3

DB_NAME = "plant_monitor.db"

# create connection
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# create plants table
def create_plants_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
        )
    """)
    
    conn.commit()
    conn.close()


#create humidity logs table
def create_humidity_logs_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS humidity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_id INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        humidity REAL NOT NULL,
        FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    conn.close()

def create_all_tables():
    create_plants_table()
    create_humidity_logs_table()
