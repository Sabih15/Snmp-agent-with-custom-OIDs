#
# PySNMP MIB module SABIH-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file:///usr/share/snmp/mibs/SABIH-MIB.txt
# Produced by pysmi-0.3.4 at Fri May 15 00:05:42 2020
# On host vbox-VirtualBox platform Linux version 5.4.0-29-generic by user vbox
# Using Python version 3.8.2 (default, Apr 27 2020, 15:53:34) 
#
OctetString, Integer, ObjectIdentifier = mibBuilder.importSymbols("ASN1", "OctetString", "Integer", "ObjectIdentifier")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueRangeConstraint, ConstraintsUnion, ValueSizeConstraint, ConstraintsIntersection, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ConstraintsUnion", "ValueSizeConstraint", "ConstraintsIntersection", "SingleValueConstraint")
NotificationGroup, ModuleCompliance = mibBuilder.importSymbols("SNMPv2-CONF", "NotificationGroup", "ModuleCompliance")
Integer32, Gauge32, Counter32, MibScalar, MibTable, MibTableRow, MibTableColumn, Bits, IpAddress, MibIdentifier, enterprises, ObjectIdentity, Unsigned32, iso, ModuleIdentity, NotificationType, TimeTicks, Counter64 = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "Gauge32", "Counter32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Bits", "IpAddress", "MibIdentifier", "enterprises", "ObjectIdentity", "Unsigned32", "iso", "ModuleIdentity", "NotificationType", "TimeTicks", "Counter64")
TextualConvention, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
afiniti = MibIdentifier((1, 3, 6, 1, 4, 1, 53864))
logSize = MibScalar((1, 3, 6, 1, 4, 1, 53864, 1), Integer32()).setMaxAccess("readonly")
if mibBuilder.loadTexts: logSize.setStatus('current')
signalValue = MibScalar((1, 3, 6, 1, 4, 1, 53864, 2), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: signalValue.setStatus('current')
versionNo = MibScalar((1, 3, 6, 1, 4, 1, 53864, 3), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: versionNo.setStatus('current')
testTrap = NotificationType((1, 3, 6, 1, 4, 1, 53864, 3))
if mibBuilder.loadTexts: testTrap.setStatus('current')
mibBuilder.exportSymbols("SABIH-MIB", afiniti=afiniti, versionNo=versionNo, testTrap=testTrap, logSize=logSize, signalValue=signalValue)
