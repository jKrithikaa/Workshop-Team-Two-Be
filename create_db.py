import sqlite3

# Create and initialize the database
def create_db():
    conn = sqlite3.connect('enquiries.db')
    cursor = conn.cursor()

    # Create the table for storing form submissions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        phone_number TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

# Call the function to create the database
create_db()
