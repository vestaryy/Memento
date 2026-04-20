import sqlite3
import os

class DatabaseAuditor:
    def __init__(self, db_path):
        self.db_path = db_path

    def check_connection(self):
        if not os.path.exists(self.db_path):
            return False, "нет бд"
        try:
            conn = sqlite3.connect(self.db_path)
            conn.close()
            return True, "всё ок"
        except Exception as e:
            return False, str(e)

    def get_general_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        u_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM content")
        c_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM content WHERE description IS NULL OR description = ''")
        empty_desc = cursor.fetchone()[0]
        
        conn.close()
        return {
            "users": u_count,
            "memories": c_count,
            "db_name": self.db_path
        }
