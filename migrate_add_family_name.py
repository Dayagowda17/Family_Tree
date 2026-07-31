"""
One-time migration: adds the 'family_name' column to the existing users table.
Run this ONCE after pulling the update, from the project root:

    python migrate_add_family_name.py

Safe to run multiple times - it checks whether the column already exists first.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'family.db')


def main():
    if not os.path.exists(DB_PATH):
        print(f"No database found at {DB_PATH} - nothing to migrate. "
              f"It will be created fresh with the new column on next app start.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cur.fetchall()]

    if 'family_name' in columns:
        print("family_name column already exists - nothing to do.")
    else:
        cur.execute("ALTER TABLE users ADD COLUMN family_name VARCHAR(100)")
        conn.commit()
        print("family_name column added successfully.")

    conn.close()


if __name__ == '__main__':
    main()
