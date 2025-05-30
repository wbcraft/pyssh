#### This is a test script to try using another server as a bastion host (jump server).  This will allow the host server to connect THROUGH a specified server to other clients.
import paramiko

def ssh_connect_via_bastion(bastion_host, bastion_username, bastion_port, target_hostname, target_username, target_port=22):
    private_key_path = "/your/id_rsa"

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

    commands = [
        #"hostname",
        #"df -h",
        #"zpool status|grep errors",
        #"uptime",
        #"date",
        #"ntpq -pn | grep '*'",
        #"pwd",
        #"python/disk_check.sh"
    ]

    for command in commands:
        stdin, stdout, stderr = target_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(f'Command Output:\n{output}')
        if error:
            print(f'Error:\n{error}')

    # Close the connections
    target_client.close()
    channel.close()
    bastion_client.close()

if __name__ == "__main__":
    hostfile_path = "/your/hosts.txt"
    username = "username"
    bastion_host = "bastion_host_name"  # Replace with your bastion host
    bastion_username = "username_again"     # Replace with your bastion user
    bastion_port = 22                       # Replace with your bastion port

    with open(hostfile_path, 'r') as hosts:
        for line in hosts:
            hostname = line.strip()
            ssh_connect_via_bastion(bastion_host, bastion_username, bastion_port, hostname, username)
