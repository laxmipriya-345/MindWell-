# reset_db.py
import sqlite3
import os

def reset_database():
    # Remove existing database if it exists
    db_path = 'mental_health.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Removed existing database: {db_path}")
    
    # Create new database with all tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Created users table")
    
    # Create mood_entries table
    cursor.execute('''
        CREATE TABLE mood_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mood_score INTEGER CHECK(mood_score >= 1 AND mood_score <= 5),
            stress_level INTEGER CHECK(stress_level >= 1 AND stress_level <= 10),
            notes TEXT,
            date DATE DEFAULT CURRENT_DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("✓ Created mood_entries table")
    
    # Create journal_entries table
    cursor.execute('''
        CREATE TABLE journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            mood_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("✓ Created journal_entries table")
    
    # Create assessments table
    cursor.execute('''
        CREATE TABLE assessments (
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
    print("✓ Created assessments table")
    
    # Create resources table (if using SQLAlchemy, this will be created separately)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resource (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Created resource table")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database initialized successfully with all tables!")

if __name__ == "__main__":
    print("=== Database Reset Tool ===\n")
    response = input("This will delete your existing database. Continue? (y/n): ")
    if response.lower() == 'y':
        reset_database()
    else:
        print("Operation cancelled.")