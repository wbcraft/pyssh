#### This is a test script to try using another server as a bastion host (jump server).  This will allow the host server to connect THROUGH a specified server to other clients.
import paramiko
import csv
from datetime import datetime

def ssh_connect_via_bastion(bastion_host, bastion_username, bastion_port, target_hostname, target_username, target_port=22):
    private_key_path = "/home/blane/.ssh/id_rsa"

    # Connect to the bastion host
    bastion_client = paramiko.SSHClient()
    bastion_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    bastion_private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    bastion_client.connect(bastion_host, username=bastion_username, pkey=bastion_private_key, port=bastion_port)

    # Create a transport through the bastion host
    transport = bastion_client.get_transport()
    channel = transport.open_channel("direct-tcpip", (target_hostname, target_port), ('localhost', 0))

    # Connect to the target host through the tunnel
    target_client = paramiko.SSHClient()
    target_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target_private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    target_client.connect(target_hostname, username=target_username, pkey=target_private_key, sock=channel)

    print(f'Connected to {target_hostname} via bastion host')
    outputs = []
    commands = [
        "hostname",
        "df -h",
        "zpool status|grep errors",
        "uptime",
        "date",
        "ntpq -pn | grep '*'",
        "pwd",
        #"python/disk_check.sh"
    ]

    for command in commands:
        stdin, stdout, stderr = target_client.exec_command(command)
        output = stdout.read().decode()
        outputs.append((command, output)) 
        error = stderr.read().decode()
        if output:
            print(f'{command} output:\n{output}')
        if error:
            print(f'Error:\n{error}')

    # Close the connections
    target_client.close()
    channel.close()
    bastion_client.close()

    return outputs

if __name__ == "__main__":
    with open('hosts.txt', 'r') as hosts:
        hostnames = [line.strip() for line in hosts]
    username = "blane"
    bastion_host = "10.0.0.144"  # Replace with your bastion host
    bastion_username = "blane"     # Replace with your bastion user
    bastion_port = 22                       # Replace with your bastion port
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    csvfile = open('outputs.csv', 'a')
    writer = csv.writer(csvfile)
    if csvfile.tell() -- 0:
        writer.writerow(['Timestamp', 'Hostname', 'Command', 'Output'])  # Write headers once

    for hostname in hostnames:
        try:
            outputs = ssh_connect_via_bastion(bastion_host, bastion_username, bastion_port, hostname, username)
            if outputs is not None:
                for command, output in outputs:
                    writer.writerow([timestamp, hostname, command, output])
        except Exception as e:
            print(f"An error occurred while processing {hostname}: {str(e)}")

    csvfile.close()
