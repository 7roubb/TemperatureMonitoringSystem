import pika
import json
import sqlite3

def fetch_switch_ips():
    conn = sqlite3.connect('switche.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM switches")
    switch_details = [[row[1], row[2], row[3]] for row in cursor.fetchall()]
    conn.close()
    return switch_details

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue')

    switch_ips = fetch_switch_ips()
    print(switch_ips)

    for ip, comm, oid in switch_ips:
        print(ip)
        task = {"task": "collect_switch_temperature", "ip": ip, 'comm': comm, 'oid': oid}
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=json.dumps(task))
        print(f" [x] Sent task to collect temperature for switch at {ip}")

    connection.close()

if __name__ == '__main__':
    main()
