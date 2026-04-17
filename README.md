# SDN-Mini-Project---Multi-Switch-Flow-Table-Analyzer
Using Mininet and OpenFlow controller (POX)

---

## Problem Statement

Analyze flow tables in SDN switches and display rule usage by identifying active and unused flows dynamically.

---

## Features

* Retrieves flow entries from multiple switches
* Displays detailed rule information (match fields, actions, packet count, bytes)
* Identifies **ACTIVE vs UNUSED** flows
* Provides **summary statistics across switches**
* Dynamically updates flow table information

---

## Tools Used

* Mininet
* POX Controller
* OpenFlow
* iperf

---

## SDN Architecture

Software Defined Networking (SDN) separates:

* **Control Plane** → POX Controller
* **Data Plane** → Open vSwitch

The controller communicates with switches using the **OpenFlow protocol**, installs flow rules, and monitors network traffic dynamically.

---

## Mininet Topology

* Linear topology with 2 switches (`s1`, `s2`)
* 2 hosts (`h1`, `h2`)
* Switch-to-switch communication enabled

```bash
sudo mn --topo linear,2 --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow10
```

---

## Controller Logic

* Handles **packet_in events** from switches
* Installs flow rules using **match–action logic**
* Uses packet count to classify flows:

  * **ACTIVE** → packet count > 0
  * **UNUSED** → packet count = 0
* Periodically requests flow statistics from switches

---

## Flow Rule Design

Each flow rule contains:

* **Match fields** (e.g., `in_port`, MAC address)
* **Actions** (forward / drop)
* **Counters**:

  * Packet count
  * Byte count

Flow rules are dynamically updated based on network traffic.

---

## Execution Steps

### 1. Clean previous Mininet setup

```bash
sudo mn -c
```

### 2. Run POX Controller

```bash
cd pox
./pox.py flow_analyzer_pox
```

### 3. Run Mininet

```bash
sudo mn --topo linear,2 --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow10
```

### 4. Test Connectivity

```bash
pingall
```

### 5. Generate Traffic

```bash
h2 iperf -s &
h1 iperf -c h2
```

---

## Output

### Detailed Flow Information

* Switch ID
* Match fields
* Actions (forward/drop)
* Packet count
* Byte count
* Duration and timeouts
* Status (**ACTIVE / UNUSED**)

### Summary Statistics

* Total flows per switch
* Active vs unused flows
* Total packets and bytes
* Rule efficiency (%)

---

## Test Cases

### 🔹 Test Case 1: No Traffic

* No packets exchanged
* Packet count = 0
* Flow status: **UNUSED**

### 🔹 Test Case 2: With Traffic

* Traffic generated using `ping` and `iperf`
* Packet count increases
* Flow status: **ACTIVE**

---

## Proof of Execution

### 🔹 Controller Startup

![POX Controller](screenshots/POX.jpeg)

### 🔹 Mininet Cleanup

![Cleanup](screenshots/sudo_mn_c.jpeg)

### 🔹 Network Connectivity (pingall)

![Connectivity](screenshots/Connectivity.jpeg)


### 🔹 Active Flow Example

![Active Flow](screenshots/Active.jpeg)

### 🔹 Unused Flow Example

![Unused Flow](screenshots/Unused.jpeg)

### 🔹 Flow Summary and Statistics

![Summary](screenshots/Summary.jpeg)

---

## Expected Output

* Flow rules displayed with detailed statistics
* Clear classification of ACTIVE and UNUSED flows
* Dynamic updates as traffic changes

---

## References

* https://mininet.org/
* https://github.com/noxrepo/pox

---

## Conclusion

This project demonstrates SDN controller-switch interaction, OpenFlow-based flow rule management, and dynamic analysis of network traffic. It effectively identifies active and unused flows while providing detailed insights into flow behavior, switch-level statistics, and overall network performance.
