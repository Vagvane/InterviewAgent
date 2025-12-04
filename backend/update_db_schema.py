import sqlite3

def update_schema():
    conn = sqlite3.connect('interview_agent.db')
    cursor = conn.cursor()
    
    try:
        # Add feedback column
        try:
            cursor.execute("ALTER TABLE interviewsession ADD COLUMN feedback JSON")
            print("Added 'feedback' column.")
        except sqlite3.OperationalError as e:
            print(f"Skipping 'feedback': {e}")

        # Add score column
        try:
            cursor.execute("ALTER TABLE interviewsession ADD COLUMN score INTEGER")
            print("Added 'score' column.")
        except sqlite3.OperationalError as e:
            print(f"Skipping 'score': {e}")
            
        conn.commit()
        print("Schema update completed.")
    except Exception as e:
        print(f"Error updating schema: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_schema()
