# Here we import paramiko, point to the private key, and print when connection is made.
# Modify the 3rd line with the path to your private key.
import paramiko
def ssh_connect(hostname, username, port=22):
    private_key_path = "/path/to/your/private/key"
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    client.connect(hostname, username=username, pkey=private_key)
    print(f'Connected to {hostname}')

#### Commands go here.
  
    commands = [
#### THESE ARE EXAMPLE COMMANDS ####
#        "df -h",
#        "zpool status|grep errors",
#        "uptime",
#        "date",
#        "ntpq -pn | grep '*'",
#        "pwd",
#        "python/disk_check.sh"   # This command checks for a script on the hostname you're connecting TO and runs it.
        "sudo apt-get update",
        "sudo apt-get upgrade -y",
        "sudo reboot"
    ]
  
#### How it parses/prints the commands.
  
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(f'{command} output:\n{output}')
        if error:
            print(f'Error:\n{error}')

    client.close()
    print('connection closed')

#### ADD YOUR HOSTS FILE AND USERNAME HERE ####

if __name__ =="__main__":
    username = "YOURUSERNAME"
    hostfile_path = "/path/to/your/hosts.txt"
    #### OR ####
    #hostname= ["hostname1", "hostname2", "hostname3",]
        #for hostname in hostnames:
    #if using this array, indent the ssh_connect line...
    with open(hostfile_path, 'r') as hosts:
        for line in hosts:
            hostname = line.strip()
            ssh_connect(hostname,username)
