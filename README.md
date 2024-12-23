SSH key howto

the integration requires ssh with out a password. 
you dont want shell access with no passwords.

here is a howto to limit a ssh key to a single remote command

on hassos make a ssh-key. I use the /config/ssh/ directory

```
\# ssh-keygen
Generating public/private ed25519 key pair.
Enter file in which to save the key (/root/.ssh/id_ed25519): /config/ssh/ssh-example
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /config/ssh/ssh-example
Your public key has been saved in /config/ssh/ssh-example.pub
The key fingerprint is:
SHA256:5eoEL28rV71Z37CyoxXq7iIY/Ge/9kJ5D9QWKNC31pQ root@a0d7b954-ssh
The key's randomart image is:
+--[ED25519 256]--+
|        .o   . . |
|          o o E  |
|          .o = . |
|         o  + +  |
|   .  . S .=..   |
|    o  o .+.+.o  |
|     +. +o...* +.|
|    . +=*.o.= o o|
|       B+BB=o+   |
+----[SHA256]-----+
```

now copy the ssh key to the designated pc with ssh

```
\# ssh-copy-id -i /config/ssh/ssh-example user@server
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/config/ssh/ssh-example.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
of a basic regular expression is not portable; it is ignored
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
user@server's password: 

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'user@server'"
and check to make sure that only the key(s) you wanted were added.
```

now on the linux server limit the added ssh key to the command you want
change the new added line `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFBzoV8LZkFBylWo36T4ElQ+IdAynJvxq+nGmObnuBoQ root@a0d7b954-ssh`
to: `command="/your/command.sh  --stdin"",restrict ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFBzoV8LZkFBylWo36T4ElQ+IdAynJvxq+nGmObnuBoQ root@a0d7b954-ssh`

this binds the ssh key to a single command. 

In home assistant create scripts for example in the /config/bin directory
```
#!/bin/bash
echo "$@" | ssh -o StrictHostKeyChecking=accept-new -i /config/ssh/<your-key> user@server 
```

now at last you can add the script to home assitant. (note: echo does something strange in ha so use the bash command)
```
  112_lookup: /config/bin/112_lookup.sh -z {{zone}} -t {{hours}}
   at5_lookup: /config/bin/at5_lookup.sh -t {{hours}}
   nu_nl_lookup: /config/bin/nu_nl_lookup.sh -t {{hours}}
   nu_nl_buitenland_lookup: /config/bin/nu_nl_buitenland_lookup.sh -t {{hours}}
```
