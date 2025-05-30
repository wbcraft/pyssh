Easy enough.  Read the script, fill in what's needed, and run it.

Both of these scripts work for me on a RPi5 host in a python venv. -Apr 1 2025 (not a joke)-

To do:

~~1) Add an array to parse a list of servers to run the commands across the environment.~~  # Added and commented Apr 1 2025 to ssh.py

~~2) Add a version for using a bastion host.~~  # Added and commented Apr 1 2025 to ssh2.py

3) Add a function to ensure data can only be read.  There will be no writing to the server(s).

~~4) Instead of using an array built into the script, use "with open" to populate a target hosts file.~~
