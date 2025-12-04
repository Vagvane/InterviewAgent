import sqlite3

def add_category_column():
    conn = sqlite3.connect('interview_agent.db')
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(question)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'category' not in columns:
            print("Adding 'category' column to 'question' table...")
            cursor.execute("ALTER TABLE question ADD COLUMN category TEXT DEFAULT 'General'")
            conn.commit()
            print("Column added successfully.")
        else:
            print("'category' column already exists.")
            
    except Exception as e:
        print(f"Error updating schema: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_category_column()
