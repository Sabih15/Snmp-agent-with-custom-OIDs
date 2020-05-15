This ReadMe file contains the methodology used to complete the task, time taken to complete the task and the list of dependencies.

## METHODOLOGY
For the tasks I opted for **Ubuntu 20.04** to remove the dependencies intricacies with **SNMP** and wrote a custom agent in **Python3** using **pysnmp** package, which then exposes custom written MIB to *SNMP Manager*.
 
 Install required packages and dependencies  
 
 `sudo apt install snmp snmp-mibs-downloader`  
 `pip3 install pysnmp`

**Note:** As I've written my own custom agent in python that's exposed by `pysnmp` package, the default `snmp` daemon (`snmpd`) isn't required for the task and make sure that it's not running and if it's stop it as it might conflicts with custom agent 

`sudo systemctl stop snmpd`

Create a MIB file which contains your enterprises and OIDs, compile it to *.py* script so that It gets exposed using `pysnmp`. Compile it using `mibdump` utility provided by `pysnmp` package  

`mibdump your-mib`

Refer to **[SABIH-MIB.txt]**

MIB file must be stored in one of the locations where mibdump looks for e.g. `/usr/share/snmp/mibs`

### AGENT
In `agent.py`, three classes were created `MIB`, `SNMPAgent`, `Worker`, worker class was to demonstrate the updating of MIB.

1. A static string was returned as versionNo; 
2. A PostgreSQL database was queried to get the `signalValue` by `signalTime` timestamp; 
3. The size used for `/var/log` was retrieved using path command `os.path.getsize()`;

After writing agent, run the agent on the machine
`sudo python3 agent.py` 
Now query the agent using manager machine, the real mojo happens here for OID 1  

`snmpwalk -m SABIH-MIB -v 2c -c public -Ct localhost .1`  

response time was ~0.06seconds (place complied mib.py file in the directory same as agent).

## TIME CONSUMPTION
* A day was consumed in downloading and installing virtualbox and ubuntu. 
* 3 days were utilized in reading and grasping the concept and understanding how to implement a custom snmp-agent and OID. 
* 2 days was used in coding the agent and writing MIB file.

## PROBLEMS FACED
 * First tried to extend the net-snmp agents but failed as no proper documentation could be found.
 * There were different formats for MIB file so finding the correct one was exhausting.
 * Faced difficulty in compiling Mib file using build-pysnmp-mib, later read that it has gone obsolete.
 * Faced issues in agent.py compilation.

## Libraries Used
 * snmp,
 * nmp-mibs-downloader
 * python3 
 * pip3
 * postgres
 * pysnmp
 * psycopg2-binary
 * mibdump
 * libsmi
