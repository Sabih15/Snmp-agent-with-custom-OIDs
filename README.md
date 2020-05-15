This ReadMe file contains the methodology used to complete the task, its time consumption, list of dependencies.

## METHODOLOGY
This is task was completed on Ubuntu operating system version 20.04 and the laguage chosen was Python programming language 3.8.2. First setup snmp on your local machine(steps below), I have written my custom agent so that I could easily use my custom MIB. After installing snmp and snmp-mibs-downloader, create a MIB file and define custom OIDs in it. Compile it to .py file using mibdump command 'mibdump <filename> (MIB file must be stored in one of the locations where mibdump looks for e.g. '/usr/share/snmp/mibs').
AGENT: In agent three classes were created 'MIb', 'SNMPAgent', 'Worker', worker class was to demonstrate the updating of Mib.
For task #1, a static string was returned as versionNo;
For task #2, a postgres db was queried to get the 'signalValue' by 'signalTime' timestamp;
For task #3, the size used for /var/log was retrived using path command 'os.path.getsize(<path>)';

After writing agent, it was executed with sudo command 'sudo python3 agent.py' and snmpwalk command was hit 'snmpwalk -m SABIH-MIB -v 2c -c public -Ct localhost .1', response time was ~0.06seconds (place complied mib.py file in the directory same as agent).

## TIME CONSUMPTION
*A day was consumed in downloading and installing virtualbox and ubuntu.
*3 days were utilized in reading and grasping the concept and understanding how to implement a custom snmp-agent and OID.
*2 days was used in coding the agent and writing MIB file.

## PROBLEMS FACED
*First tried to extend the snmpd and net-snmp agents but failed as no proper documentation could be found;
*There were different formats for MIB file so finding the correct one was exhausting;
*Faced difficulty in compiling Mib file using build-pysnmp-mib, later read that it has gone obsolete;
*Faced issues in agent.py compilation.

## DEPENDENCIES
*snmp, snmp-mibs-downloader
*python3
*pip3
*postgres
*pysnmp, psycopg2-binary, mibdump, libsmi

#HOW TO SETUP SNMP AND MIB ON LOCAL MACHINE##
1. Update packages using sudo apt-get update.
2. Install the snmp software using command 'sudo apt install snmp'.
3. Install the snmp-libs-downloader using command 'sudo apt install 'snmp-mibs-downloader'.
*snmpd is not required as we used our own custom agent.
