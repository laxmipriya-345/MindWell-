# init_db.py
import sqlite3
from database import init_db as init_db_function

def create_assessments_table():
    conn = sqlite3.connect('mental_health.db')
    cursor = conn.cursor()
    
    # Create assessments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            responses TEXT,
            date TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Assessments table created successfully!")

if __name__ == "__main__":
    print("Initializing database...")
    create_assessments_table()
    print("Database initialization complete!")