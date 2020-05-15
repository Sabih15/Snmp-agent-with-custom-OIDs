from pysnmp.entity import engine, config
from pysnmp import debug
from pysnmp.entity.rfc3413 import cmdrsp, context, ntforg
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.smi import builder
from pathlib import Path
import os
import psycopg2

import threading
import collections
import time

#can be useful
#debug.setLogger(debug.Debug('all'))

MibObject = collections.namedtuple('MibObject', ['mibName',
                                   'objectType', 'valueFunc'])
                                   


class Mib(object):

    def __init__(self):
        self._lock = threading.RLock()
        self._log_size = 0

    def getVersionNo(self):
        return "6.1.1"
        
    def getSignalValue(self):
        return self.executeScript()

    def getLogSize(self):
        with self._lock:
            return self.get_size()
            
    def executeScript(self):
        try:
            connection = psycopg2.connect(user= 'admin',password= 'Tekno_2018',host= 'localhost',port= '5432',database= 'afinitiTest')
            cursor = connection.cursor()
            os.chdir('/home/vbox/Downloads')
            f = open('/home/vbox/Downloads/dbscript.sql', 'r')
            sqlfile = f.read()
            f.close()
            commands = sqlfile.split(';')
            print(len(commands))
            for command in commands:
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(e)
            
            cursor.execute('SELect signalValue FROM snmpSignals WHERE signalTime = (SELECT MAX(signalTime) FROM snmpSignals) ORDER BY id desc fetch first 1 rows only')
            val = ''
            res = cursor.fetchall()
            print(res)
            for r in res:
                val = r[0]
            return val
                        
        except Exception as e: 
            print(e)
            
    def get_size(start_path = '/var/log'):
        total_size = 0
        os.chdir('/var/log')
        total_size = os.path.getsize('/var/log')
        return total_size

    def setLogSize(self, value):
        with self._lock:
            self._test_count = value


def createVariable(SuperClass, getValue, *args):
    #This is going to create a instance variable that we can export. 
    #getValue is a function to call to retreive the value of the scalar
    class Var(SuperClass):
        def readGet(self, name, *args):
            return name, self.syntax.clone(getValue())
    return Var(*args)


class SNMPAgent(object):
    #Implements an Agent that serves the custom MIB and
    #can send a trap.
    

    def __init__(self, mibObjects):
        
        #each SNMP-based application has an engine
        self._snmpEngine = engine.SnmpEngine()

        #open a UDP socket to listen for snmp requests
        config.addSocketTransport(self._snmpEngine, udp.domainName,
                                  udp.UdpTransport().openServerMode(('', 161)))

        #add a v2 user with the community string public
        config.addV1System(self._snmpEngine, "agent", "public")
        #let anyone accessing 'public' read anything in the subtree below,
        #which is the enterprises subtree that we defined our MIB to be in
        config.addVacmUser(self._snmpEngine, 2, "agent", "noAuthNoPriv",
                           readSubTree=(1,3,6,1,4,1))

        #each app has one or more contexts
        self._snmpContext = context.SnmpContext(self._snmpEngine)

        #the builder is used to load mibs. tell it to look in the
        #current directory for our new MIB. We'll also use it to
        #export our symbols later
        mibBuilder = self._snmpContext.getMibInstrum().getMibBuilder()
        mibSources = mibBuilder.getMibSources() + (builder.DirMibSource('.'),)
        mibBuilder.setMibSources(*mibSources)

        #our variables will subclass this since we only have scalar types
        #can't load this type directly, need to import it
        MibScalarInstance, = mibBuilder.importSymbols('SNMPv2-SMI',
                                                      'MibScalarInstance')
        #export our custom mib
        for mibObject in mibObjects:
            nextVar, = mibBuilder.importSymbols(mibObject.mibName,
                                                mibObject.objectType)
            instance = createVariable(MibScalarInstance,
                                      mibObject.valueFunc,
                                      nextVar.name, (0,),
                                      nextVar.syntax)
            #need to export as <var name>Instance
            instanceDict = {str(nextVar.name)+"Instance":instance}
            mibBuilder.exportSymbols(mibObject.mibName,
                                     **instanceDict)

        # tell pysnmp to respond to get, getnext, and getbulk
        cmdrsp.GetCommandResponder(self._snmpEngine, self._snmpContext)
        cmdrsp.NextCommandResponder(self._snmpEngine, self._snmpContext)
        cmdrsp.BulkCommandResponder(self._snmpEngine, self._snmpContext)


    def setTrapReceiver(self, host, community):
        """Send traps to the host using community string community
        """
        config.addV1System(self._snmpEngine, 'nms-area', community)
        config.addVacmUser(self._snmpEngine, 2, 'nms-area', 'noAuthNoPriv',
                           notifySubTree=(1,3,6,1,4,1))
        config.addTargetParams(self._snmpEngine,
                               'nms-creds', 'nms-area', 'noAuthNoPriv', 1)
        config.addTargetAddr(self._snmpEngine, 'my-nms', udp.domainName,
                             (host, 162), 'nms-creds',
                             tagList='all-my-managers')
        #set last parameter to 'notification' to have it send
        #informs rather than unacknowledged traps
        config.addNotificationTarget(
            self._snmpEngine, 'test-notification', 'my-filter',
            'all-my-managers', 'trap')


    def sendTrap(self):
        print ("Sending trap")
        ntfOrg = ntforg.NotificationOriginator(self._snmpContext)
        errorIndication = ntfOrg.sendNotification(
            self._snmpEngine,
            'test-notification',
            ('SABIH-MIB', 'testTrap'),
            ())


    def serve_forever(self):
        print ("Starting agent")
        self._snmpEngine.transportDispatcher.jobStarted(1)
        try:
           self._snmpEngine.transportDispatcher.runDispatcher()
        except:
            self._snmpEngine.transportDispatcher.closeDispatcher()
            raise

class Worker(threading.Thread):
    """Just to demonstrate updating the MIB
    and sending traps
    """

    def __init__(self, agent, mib):
        threading.Thread.__init__(self)
        self._agent = agent
        self._mib = mib
        self.setDaemon(True)

    def run(self):
        while True:
            time.sleep(3)
            self._mib.setLogSize(mib.getLogSize()+1)
            #self._agent.sendTrap()

if __name__ == '__main__':
    mib = Mib()
    objects = [MibObject('SABIH-MIB', 'versionNo', mib.getVersionNo),
               MibObject('SABIH-MIB', 'signalValue', mib.getSignalValue),
               MibObject('SABIH-MIB', 'logSize', mib.getLogSize)]
    agent = SNMPAgent(objects)
    Worker(agent, mib).start()
    try:
        agent.serve_forever()
    except KeyboardInterrupt:
        print ("Shutting down")

