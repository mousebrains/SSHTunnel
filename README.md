# SSH Tunnel so a computer on one side of a firewall can connect to a computer on the other side

Using `ssh` create a tunnel from the ship side computer 
to the shore side computer 
so a connection can be originated from shore to ship.

On the shore side computer change the sshd config needs the `clientAliveInterval` and `clientAliveCount` need to be set to keep the connection up. On an Ubuntu system, copy 010.ClientAlive.conf to the `/etc/ssh/sshd_config.d` directory and restart the sshd daemon.
