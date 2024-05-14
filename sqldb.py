import sqlite3

def create_database():
    conn = sqlite3.connect('switches.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS switches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT NOT NULL,
        community_string TEXT NOT NULL,
        oid TEXT NOT NULL
    )
    ''')
    
    # List of IP addresses to add
    ip_addresses = [
        ['127.0.0.5','Cisco3750', '1.3.6.1.4.1.9.9.91.1.1.1.1.4.1062'],
        ['127.0.0.6','Cisco3750', '1.3.6.1.4.1.9.9.91.1.1.1.1.4.1062'],
        ['127.0.0.7','Cisco3750', '1.3.6.1.4.1.9.9.91.1.1.1.1.4.1062'],
        ['127.0.0.8','Cisco3750', '1.3.6.1.4.1.9.9.91.1.1.1.1.4.1062'],
        ['127.0.0.9','Cisco3750', '1.3.6.1.4.1.9.9.91.1.1.1.1.4.1062'],
    ]

    cursor.executemany('INSERT INTO switches (ip_address,community_string,oid) VALUES (?,?,?)', [(ip,community_string,oid) for ip, community_string, oid in ip_addresses])

    conn.commit()
    conn.close()

    print("Database and table created successfully, and IP addresses added.")

if __name__ == '__main__':
    create_database()
