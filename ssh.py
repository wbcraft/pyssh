# Here we import paramiko, point to the private key, and print when connection is made.

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
#        "pwd",
#        "python/disk_check.sh"   # This command checks for a script on the hostname you're connecting TO and runs it.
    ]
  
#### How it parses/prints the commands.
  
    for command in commands:
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if output:
            print(f'Command Output:\n{output}')
        if error:
            print(f'Error:\n{error}')

    client.close()
    print('connection closed')

#### ADD YOUR HOSTNAME AND USERNAME HERE ####

if __name__ =="__main__":
    hostname = "YOURHOSTNAME" 
    username = "YOURUSERNAME"

    ssh_connect(hostname,username)
