import sqlite3
import datetime
import collections

class ActivityTracker:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_time_report(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT created_date FROM content")
        raw_dates = [row[0] for row in cursor.fetchall()]
        conn.close()

        weekdays = []
        hours = []

        for d_str in raw_dates:
            try:
                clean_date = d_str.split('.')[0]
                dt = datetime.datetime.fromisoformat(clean_date)
                weekdays.append(dt.strftime('%A'))
                hours.append(dt.hour)
            except Exception:
                continue

        return {
            "days_dist": collections.Counter(weekdays),
            "hours_dist": collections.Counter(hours)
        }
