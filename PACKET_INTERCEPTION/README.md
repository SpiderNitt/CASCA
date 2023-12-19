# Packet Interception on real interfaces

Run everything with the root privilege

```
$ python3 -m venv .
$ source bin/activate
$ pip install -r requirements.txt 
```

Configure Iptable for the packet interception
```
$ ./shell/iptables.sh
```