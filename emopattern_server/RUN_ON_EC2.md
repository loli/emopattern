# Run on AWS EC2

# Stable diffusion modle to run
SD XL Turbo (downloaded automatically)

# EC2 instance

## Instance type
g4dn.xlarge - https://aws.amazon.com/ec2/instance-types/

## Instance image
https://aws.amazon.com/releasenotes/aws-deep-learning-ami-gpu-pytorch-2-0-amazon-linux-2/ (ami-0aae764a1f6a4b68c)

## Connectivity
- With key-pair to ssh into the machine.
- SHH open from everywhere or 10.4.0.0/16 (staging VPN)

# Storage
100GB GP3

## Connect (ssh)
Look up instance's "Hostname type", e.g.: IP name: ip-10-19-6-51.eu-west-1.compute.internal

`ssh -i ~/<your-keyfile>.pem ec2-user@ip-10-19-6-51.eu-west-1.compute.internal`

# IP and security
Edit the instance's [Security Group](https://eu-west-1.console.aws.amazon.com/ec2/home?region=eu-west-1#SecurityGroups:) to allow custom TCP inbound traffic.
```
IP version  Type        Protocol    Port range  Source                      Description
IPv4	    Custom TCP	TCP	        5556	    10.4.0.0/16 (staging VPN)   zeromq
```

## Installation
Follow instruction in [README.md](README.md). Might require you to run:

```
sudo yum install alsa-lib-devel
sudo amazon-linux-extras install epel -y
sudo yum install -y portaudio-devel portaudio
```

# How to run
- One computer with `viewer` app
- Supply IP of viewer machine to server (as `ip_viewer`)
- Run server app
- Supply server machine's (private) IP to detector `app`
- Run deterctor app (requires staging VPN)

## Tips
- Might need port forwarding in viewer app network to viewer app PC (TCP, 5557)
- Detector `app` should be in staging VPN
- Test if ZMQueque is reachabe & listening with `telnet <ip> <port>`
