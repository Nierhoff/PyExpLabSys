import time
import serial
import random

class SCPI:

    def __init__(self,device,port):
        self.device = device
        self.port = port
        try:
            if self.port == 'file':
                self.f = open(self.device, 'w')
                self.f.close()
            if self.port == 'serial':
                self.f = serial.Serial(self.device, 9600, timeout=1,xonxoff=True)
            self.debug = False
        except Exception,e:
            self.debug = True
            print "Debug mode: " + str(e)

    def scpi_comm(self,command):
        #print self.f.xonxoff
        return_string = ""
        if self.debug:
            return str(random.random())
        if self.port == 'file':
            self.f = open(self.device, 'w')
            self.f.write(command)
            time.sleep(0.02)
            self.f.close()
            time.sleep(0.1)

            if command.endswith('?'):
                self.f = open(self.device, 'r')
                return_string = self.f.readline()
                self.f.close()
                
        if self.port == 'serial':
            self.f.write(command + '\n')
            time.sleep(0.05) 
            if command.endswith('?'):
                if self.f.inWaiting()==0:
                    #print "wait!!!!!!!!!!!!!!!: " + command
                    return_string = "-99999999"
            while self.f.inWaiting()>0:
                return_string += self.f.read(1)
        return return_string
    
    def ReadSoftwareVersion(self, short=False):
        version_string = self.scpi_comm("*IDN?")
        return(version_string)    
    
    def ResetDevice(self):
        self.scpi_comm("*RST")
        return(True)

    def DeviceClear(self):
        self.scpi_comm("*abort")
        return(True)

    def ClearErrorQueue(self):
        error = self.scpi_comm("*ESR?")
        self.scpi_comm("*cls")
        return(error)
