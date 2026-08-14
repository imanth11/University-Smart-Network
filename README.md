# University Smart Network & Disaster Recovery System

A complete Cisco Packet Tracer project that models a multi-department university network with dynamic routing, centralized network services, service monitoring, redundancy testing, and an IoT-based emergency response system.

The project combines traditional enterprise networking concepts with programmable end devices and IoT automation to demonstrate both **network availability** and **disaster recovery** inside a single Packet Tracer topology.

## Overview

The simulated university is divided into four logical LANs:

- **Academic**
- **Admin**
- **Library**
- **Data Center**

Four routers form a redundant routed topology and exchange routes using **OSPF**. Centralized services are hosted in the Data Center and are reachable from the user networks through dynamic routing.

The project also includes two programmable components:

1. **University Network Management Console** - checks the availability of DNS, Web, Mail, FTP/File, and DHCP services.
2. **IoT Disaster Recovery System** - monitors temperature and smoke and automatically activates emergency devices when a fire condition is detected.

## Key Features

### Network Infrastructure

- Four independent `/24` LANs
- Four-router redundant topology
- OSPF dynamic routing
- Automatic route recovery after link failure
- Point-to-point `/30` router links
- Inter-LAN connectivity
- Centralized Data Center services

### Network Services

- DHCP
- DNS
- HTTP Web Server
- SMTP / POP3 Mail Server
- FTP File Server

### Management & Monitoring

- Programmable University Network Management Console
- HTTP-based DNS and Web checks
- TCP-based Mail and FTP service checks
- DHCP validation based on the assigned client address
- Consolidated health report for all monitored services

### IoT Disaster Recovery

- Temperature monitoring
- Smoke detection
- Automatic fire/emergency state
- Red and green status LEDs
- Alarm activation
- Emergency fan control
- Automatic emergency-door opening
- LCD status messages
- Automatic recovery when the hazardous condition is removed

## Project Files

```text
FinalProject/
├── FInalProject.pkt          # Main Cisco Packet Tracer topology
├── ConsoleManagement.py     # Network service monitoring logic
├── Iot.py                   # IoT emergency/recovery controller
└── FinalReport.pdf          # Full project documentation and test evidence
```

> **Note:** The `.py` files use Cisco Packet Tracer's built-in programming APIs such as `tcp`, `http`, `networking`, and `gpio`. They are intended to run inside Packet Tracer programmable devices and are not standalone CPython scripts.

## Requirements

- Cisco Packet Tracer with support for:
  - routing and OSPF,
  - server services,
  - programmable end devices,
  - MCU-PT / IoT components,
  - Python-based Packet Tracer APIs.

No external Python packages are required because the scripts run inside Packet Tracer's simulation environment.

## Network Architecture

### LAN Addressing

| Department | Network | Default Gateway |
|---|---|---|
| Academic | `192.168.10.0/24` | `192.168.10.1` |
| Admin | `192.168.20.0/24` | `192.168.20.1` |
| Library | `192.168.30.0/24` | `192.168.30.1` |
| Data Center | `192.168.40.0/24` | `192.168.40.1` |

### Router Interconnections

The routers are connected using dedicated `/30` point-to-point networks:

| Link | Side A | Side B |
|---|---|---|
| R1 - R2 | `10.0.12.1/30` | `10.0.12.2/30` |
| R2 - R3 | `10.0.23.1/30` | `10.0.23.2/30` |
| R3 - R4 | `10.0.34.1/30` | `10.0.34.2/30` |
| R4 - R1 | `10.0.41.1/30` | `10.0.41.2/30` |

This ring-style layout provides an alternative path when one router-to-router link becomes unavailable.

## Data Center Services

| Service | IP Address | Purpose |
|---|---|---|
| DHCP Server | `192.168.40.10` | Dynamic client addressing |
| DNS Server | `192.168.40.11` | Name resolution |
| Web Server | `192.168.40.12` | University website |
| Mail Server | `192.168.40.13` | SMTP / POP3 email |
| File Server | `192.168.40.14` | FTP file transfer |

### DNS Records

The topology includes the following service names:

| Hostname | Address |
|---|---|
| `www.university.local` | `192.168.40.12` |
| `mail.university.com` | `192.168.40.13` |
| `files.university.local` | `192.168.40.14` |

## DHCP Design

The central DHCP server contains separate address pools for the main user networks.

| Pool | Starting Address | Gateway | DNS Server |
|---|---|---|---|
| Academic | `192.168.10.100` | `192.168.10.1` | `192.168.40.11` |
| Admin | `192.168.20.100` | `192.168.20.1` | `192.168.40.11` |
| Library | `192.168.30.100` | `192.168.30.1` | `192.168.40.11` |

Routers connected to remote client LANs forward DHCP requests to the central server using `ip helper-address`.

## OSPF & Redundancy

OSPF is used to advertise the LAN and inter-router networks dynamically.

The topology is intentionally redundant. If the direct link between two neighboring routers is shut down, OSPF reconverges and traffic can continue through the alternate side of the router ring.

A demonstrated failure scenario is the R1-R2 link outage. After the link is disabled, traffic can be rerouted through:

```text
R1 -> R4 -> R3 -> R2
```

This verifies that the network can maintain connectivity after a single inter-router link failure.

## University Network Management Console

`ConsoleManagement.py` provides a lightweight service-health dashboard inside Packet Tracer.

It checks five critical services:

| Check | Method |
|---|---|
| DNS | Opens `http://www.university.local` |
| Web Server | HTTP request to `192.168.40.12` |
| Mail Server | TCP connection to `192.168.40.13:25` |
| File Server | TCP connection to `192.168.40.14:21` |
| DHCP | Verifies the local address is in the Academic DHCP range |

The console reports each service as either:

```text
Online - Success
```

or:

```text
Offline - Failed
```

It then calculates an overall status:

- `SUCCESS` - all five services are online
- `WARNING` - one or more services are unavailable
- `FAILED` - all monitored services are unavailable

### Management Console Options

The script contains the following menu logic:

```text
1. Check DNS
2. Check Web Server
3. Check Mail Server
4. Check File Server
5. Check DHCP
6. Overall Service Report
7. Exit
```

Because interactive `input()` handling is limited in Packet Tracer's Python environment, the selected action is controlled by the `choice` variable near the top of `ConsoleManagement.py`.

For example:

```python
choice = 6
```

runs the complete service report.

## IoT Disaster Recovery System

`Iot.py` implements an automated fire-response controller using an MCU-PT device.

### MCU Pin Mapping

| Device | MCU Pin | Function |
|---|---:|---|
| Temperature Sensor | `A0` | Temperature input |
| Smoke Sensor | `A1` | Smoke detection |
| Red LED | `D0` | Emergency indicator |
| Green LED | `D1` | Normal-state indicator |
| Alarm | `D2` | Audible alarm |
| Fan | `D3` | Emergency ventilation |
| Door | `D4` | Emergency exit control |
| LCD / Display | `D5` | System-status output |

### Emergency Condition

Emergency mode is activated when both conditions are true:

```text
Temperature > 45 C
AND
Smoke detected
```

When an emergency is detected, the controller automatically:

- turns the red LED on,
- turns the green LED off,
- activates the alarm,
- starts the fan,
- opens the emergency door, and
- changes the display to `EMERGENCY - FIRE`.

### Automatic Recovery

The controller continuously monitors the sensors. When the emergency condition is no longer present, the system returns to normal operation without restarting the program.

Recovery mode:

- turns the alarm off,
- turns the red LED off,
- turns the green LED on,
- stops the fan,
- closes the door, and
- restores the display to `SYSTEM NORMAL`.

## How to Run the Project

### 1. Open the Packet Tracer Topology

Launch Cisco Packet Tracer and open:

```text
FInalProject.pkt
```

### 2. Allow the Network to Converge

Use Realtime mode and allow enough time for:

- interfaces to come up,
- OSPF neighbor relationships to form,
- routes to populate, and
- DHCP clients to receive addresses.

### 3. Verify Client Addressing

On clients in the Academic, Admin, and Library networks, open **Desktop > IP Configuration** and confirm that DHCP has assigned the correct:

- IP address,
- subnet mask,
- default gateway, and
- DNS server.

### 4. Test Network Connectivity

Use `ping` and `tracert` / `traceroute` between client networks and Data Center servers.

Examples:

```text
ping 192.168.40.12
ping 192.168.40.14
```

### 5. Test DNS and Web Services

From a client browser, open:

```text
http://www.university.local
```

### 6. Test FTP and Mail Services

Use the Packet Tracer client applications or command-line tools to verify FTP and email connectivity.

### 7. Run the Management Console

Open the programmable Management Console device, load/run `ConsoleManagement.py`, select the required action through the `choice` variable, and inspect the console output.

### 8. Test OSPF Failover

Disable one inter-router link and verify that:

- the OSPF adjacency changes,
- routes reconverge, and
- end-to-end connectivity remains available through the alternate route.

Re-enable the link afterward and verify that the OSPF neighbor relationship returns to `FULL`.

### 9. Test the IoT Emergency Scenario

In Physical / Environment mode:

1. Increase the simulated temperature above `45 C`.
2. Set smoke to a non-zero value.
3. Confirm that the MCU changes to emergency mode.
4. Remove the smoke or reduce the hazard condition.
5. Confirm automatic recovery to normal mode.

## Expected Management Console Output

A healthy network produces output similar to:

```text
----------------------------------------
University Network Service Report
----------------------------------------
DNS: Online - Success
Web Server: Online - Success
Mail Server: Online - Success
File Server: Online - Success
DHCP: Online - Success
----------------------------------------
Online Services: 5/5
Overall: SUCCESS - All services online
----------------------------------------
```

## Validation Scenarios

The project demonstrates the following end-to-end scenarios:

- DHCP assignment in multiple LANs
- DNS name resolution
- Web service access
- SMTP / POP3 mail availability
- FTP upload/download connectivity
- communication between different LANs
- OSPF neighbor establishment
- dynamic route learning
- OSPF failover after a link outage
- centralized service monitoring
- IoT fire detection
- emergency actuator control
- automatic disaster-recovery transition

## Technical Notes

- The Management Console is intentionally adapted to Packet Tracer's restricted Python runtime.
- `ConsoleManagement.py` should be executed inside the Packet Tracer programmable end-device environment.
- `Iot.py` should run on the MCU-PT associated with the connected sensors and actuators.
- The service IP addresses, ports, and DHCP range are hard-coded to match the supplied topology. If the network addressing is changed, the monitoring script should be updated accordingly.
- Packet Tracer is a simulation environment; behavior and protocol timing may differ from production Cisco hardware.

## Possible Extensions

Future improvements could include:

- VLAN segmentation and inter-VLAN routing,
- ACL-based access control between departments,
- SSH-based router administration,
- SNMP-style monitoring,
- centralized logging / syslog,
- redundant Data Center services,
- additional IoT hazards and sensors,
- automatic notification during emergency events,
- a richer interactive management dashboard.

## Academic Purpose

This project is intended for educational use and demonstrates practical integration of routing, addressing, centralized services, fault tolerance, programmable monitoring, and IoT automation in Cisco Packet Tracer.
