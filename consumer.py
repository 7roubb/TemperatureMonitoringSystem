import pika
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import subprocess
import random 
from dotenv import load_dotenv
import os

load_dotenv()

Email:str= os.getenv('EMAIL')
Password:str= os.getenv('PASSWORD')

def collect_switch_temperature(ip_address:str, comm:str, oid:str):
    cmd = subprocess.run(['snmpget -v 2c -c {} {}:1611 {}'.format(comm, ip_address, oid)],capture_output=True, shell=True)
    after_exe:str = str(cmd.stdout)
    temp = int(after_exe.split('INTEGER: ')[1].split('\\n')[0])
    return random.randrange(temp - 40, temp + 40)

bucket = "Project2"
org = "PPU"
token = "LmTPOiQdAzFz9FtJkgQvyUqObRdLrPRegL8lSzOp5zob1zk9IpnykmVJbwC-IOXqSd22pLTdMiFms4QOIKli7g=="
url = "https://us-east-1-1.aws.cloud2.influxdata.com/"
def write_to_influxdb(switch_ip, temperature):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    point = (
        Point("switch_temperature")
        .tag("switch_ip", switch_ip)
        .field("temperature", float(temperature))
        .time(time.time_ns(), WritePrecision.NS)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    client.close()
    
def sendEmail(ip, temp):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587 
    sender_email = Email
    receiver_email = "7roubb@gmail.com"
    username = Email
    password = Password
    subject = "Tempreture Alert"
    body = "The switch tempreture with ip {} has became {}.".format(ip, temp)
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(" [-] Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    

def callback(ch, method, properties, body):
    task = json.loads(body)
    if task['task'] == 'collect_switch_temperature':
        print(f" [x] Received task to collect temperature for switch at {task['ip']}")
        temperature = collect_switch_temperature(task['ip'], task['comm'], task['oid'])
        if temperature:
            print(f" [x] Temperature for switch {task['ip']}: {temperature}°C")
            if(temperature > 110):
                sendEmail(task['ip'], temperature)
            write_to_influxdb(task['ip'], temperature)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('---------------------------')

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue')
    channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=False)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
