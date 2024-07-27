
## Index

1. Basics
2. OSI Model
3. TCP/IP
4. UDP
5. IPv4/IPv6
6. NAT
7. Certificates
8. Sockets
9. VLANS/Subnets
10. ARP
11. DHCP
12. CDN
13. NTP

## Basics

**What is a Network?**
A system that allows multiple devices to communicate with each other.

**How to connect devices?**
A switch is used to connect devices. An example of switch is WiFi. Wireless devices usually connect to a wireless Access Point (AP). Sometimes wireless computers will connect to each other without an AP. This is called an **AdHoc** network.

**Protocol**
Devices in order to talk to each other needs to use the same language or rules. This is called a protocol. Some examples are HTTP, SMTP, TCP, Ethernet etc

**How many protocols are used when one computer accesses another computer?**
Several protocols may work together to accomplish a task

**Your company has three divisions. Each group has a network, and all the networks are joined together. Is this still a LAN? Or is it something else?**
If each group has their own network, each network could be called a LAN. If these networks are joined together, this could also be called a LAN

**The company adds a retail division. There is a head office and six branch offices. What type of network is this?**
All the components of the network in the head office are in a local area, so this part would be called a LAN. Each of the branch offices would also be called a LAN.
But, all of these networks are separated, so the whole network would not be called a LAN.
If the offices were connected together, this part of the network would be called a WAN. The WAN is the parts that connect the offices together.
Normally, a service provider would be used to provide some or all of the equipment for these connections.
As a whole, this would be called an enterprise network

Different types of Networks:
1. SOHO: Small Office, Home Office. Small number of devices. Usually use router to connect to the internet.
2. Enterprise: May cover multiple floors, buildings and difference offices from multiple locations
3. SMB: Small Medium Business
4. Internet/Service Provider Network: 
5. LAN: No specific definition but it is part of network which is confined to local area. Like devices on SOHO maybe part of LAN or each floor n Enterprise of SMB may be part of LAN
6. WAN: Wide Area Network. Covers larger area

Ethernet:
Wired LAN uses a protocol called Ethernet. A layer in this protocol called media access control (MAC) controls how the media is formatted. Physical layer controls how the message is transmitted.

IEEE standards
802 = LAN technologies
802.3xx = Ethernet
802.3an = 10GBASE-T: 10G = 10Gbps, BASE = Baseband(cables) with digital signal, T= UTP(unshielded twisted pair) cables. Modern UTP cables has 4 cables, each pair is a circuit. Twisting prevents crosstalk which happens because of electric field. These cables are names like cat2, cat4, cat5e, cat6, at6a, cat7
cat5 = 100Mb
cat5e = 1Gbps
cat6 = 10Gbps upto 55m
cat6a = 10Gbps upto 100m

RJ45 connector
This connector is used to connect host to a switch. There are 4 pairs of wires. Some are used for Transmission(TX) and some for Reception(RX). When a host is connected to a switch, a straight through cable is used where TX and RX lines up with host and switch. But if we need to connect host to host or switch to switch then we need to use crossover cables where TX and RX are crossed.
In modern computers we don't need to care about the type of cable as auto MDI-X matches the TX and RX logically.
In some newer standards like 1000BASE-T all pins are used for TX and RX and may need newer cables like cat5e

Fiber Cables
Based on software, device and cable, it can be full duplex where devices can receive and send at the same time or half duplex where they can only do one thing at a time. A single fiber cable is called single core and supports half duplex and two cables are called 2 cores and  support full duplex.

Types of fiber cables:

| Single Mode Fiber | Multi Mode Fiber |
| ----------------- | ---------------- |
| SMF               | MMF              |
| Laser Light       | LED Light        |
| > 2km             | 500m             |
| More Expensive    | Cheaper          |
Bend Radius
Fiber cables have bend radius. If it is bended beyond this radius the signals starts attenuating.

Wifi
Wifi uses access points instead of cables and acts like a switch which host like smartphones connect to. It uses 802.11 standard. Ethernet and Wifi have similarities with how to format messages.

LAN
Each device gets an IP address and a MAC address. Each device gets atleast one MAC address which is burned in and permanent one. MAC address is used to locate within a LAN. IP address can be used within a LAN segment but usually used to pass traffic to a different segment