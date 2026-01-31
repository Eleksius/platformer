import csv
import os
import sqlite3

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

CSV_PATH = os.path.join(DATA_DIR, 'scores.csv')
DB_PATH = os.path.join(DATA_DIR, 'scores.db')


def save_score(entry, format='csv'):
    # entry: (name, score)
    if format == 'csv':
        existed = os.path.exists(CSV_PATH)
        with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not existed:
                writer.writerow(['name', 'score'])
            writer.writerow(entry)
    elif format == 'sqlite':
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS scores (name TEXT, score INTEGER)')
        c.execute('INSERT INTO scores (name, score) VALUES (?, ?)', entry)
        conn.commit()
        conn.close()


def load_scores(format='csv'):
    results = []
    if format == 'csv':
        if os.path.exists(CSV_PATH):
            with open(CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    results.append((row['name'], int(row['score'])))
    elif format == 'sqlite':
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            for row in c.execute('SELECT name, score FROM scores ORDER BY score DESC'):
                results.append(row)
            conn.close()
    # sort descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results
