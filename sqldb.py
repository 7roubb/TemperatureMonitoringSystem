import sqlite3

def create_database():
    conn = sqlite3.connect('switches.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS switches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT NOT NULL
    )
    ''')

    # List of IP addresses to add
    ip_addresses = [
        '192.168.1.1',
        '192.168.1.2',
        '192.168.1.3',
        '192.168.1.4',
        '192.168.1.5'
    ]

    cursor.executemany('INSERT INTO switches (ip_address) VALUES (?)', [(ip,) for ip in ip_addresses])

    conn.commit()
    conn.close()

    print("Database and table created successfully, and IP addresses added.")

if __name__ == '__main__':
    create_database()
