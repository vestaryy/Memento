import sqlite3
import re
import collections
from statistics import mean

class SemanticAnalyzer:
    def __init__(self, db_path):
        self.db_path = db_path
        self.stop_words = ['и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а']

    def fetch_descriptions(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM content")
        data = [row[0] for row in cursor.fetchall() if row[0]]
        conn.close()
        return data

    def get_text_metrics(self):
        texts = self.fetch_descriptions()
        if not texts:
            return None

        lengths = [len(t) for t in texts]
        all_text = " ".join(texts).lower()
        words = re.findall(r'\w+', all_text)
        filtered = [w for w in words if w not in self.stop_words and len(w) > 2]

        return {
            "avg_len": round(mean(lengths), 2),
            "max_len": max(lengths),
            "min_len": min(lengths),
            "total_chars": sum(lengths),
            "top_words": collections.Counter(filtered).most_common(10)
        }

    def get_most_common_words(self, limit=10):
        texts = self.fetch_descriptions()
        all_text = " ".join(texts).lower()
        words = re.findall(r'\w+', all_text)
        filtered = [w for w in words if w not in self.stop_words and len(w) > 2]
        return collections.Counter(filtered).most_common(limit)
