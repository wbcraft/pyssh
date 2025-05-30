### Description:

Easy enough.  Read the script, fill in what's needed, and run it.

Both of these scripts work for me on a RPi5 host in a python venv. -Apr 1 2025 (not a joke)-

Also tested on Debian 11 and it seems to work fine.
\
\
\

### To do:

~~1) Add an array to parse a list of servers to run the commands across the environment.~~  # Added and commented Apr 1 2025 to ssh.py

~~2) Add a version for using a bastion host.~~  # Added and commented Apr 1 2025 to ssh2.py

3) Add a function to ensure data can only be read.  There will be no writing to the server(s).

~~4) Instead of using an array built into the script, use "with open" to populate a target hosts file.~~
\
\
\

### Installation:

1) Create a python venv.
   
   a) mkdir python && cd python

   b) python -m venv ssh

   c) cd ssh

3) Activate the venv.

   a) source bin/activate

4) Install paramiko.

   a) pip3 install paramiko

5) Create and edit the hosts file.

6) Modify the script for your username, private key location, etc...  Remember the bastion host and bastion host username if you're using the ssh2.py

7) Send it.
