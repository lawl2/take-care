import serial
import serial.tools.list_ports
import time
import requests
import numpy as np
import urllib.request

#port of Arduino
PORTNAME='COM5'


ADAFRUIT_IO_USERNAME = "lawl"
ADAFRUIT_IO_KEY = "aio_kEAA97nF0YNtiC2nrZNGQCb42QX0"



class Bridge():

    def setupSerial(self):
        # open serial port
        self.ser = None
        print("list of available ports: ")

        ports = serial.tools.list_ports.comports()
        self.portname = None
        for port in ports:
            print(port.device)
            print(port.description)
            if 'arduino' in port.description.lower():
                self.portname = port.device
        print("connecting to " + self.portname)

        try:
            if self.portname is not None:
                self.ser = serial.Serial(self.portname, 9600, timeout=0)
        except:
            self.ser = None

        # self.ser.open()

        # internal input buffer from serial
        self.inbuffer = []


    def setup(self):
        self.setupSerial()

    def loop(self):
        # infinite loop
        val = ['0','0']
        feedname = ['tempsensor', 'watsensor']
        lasttime = time.time()
        while (True):

            if not self.ser is None:
                #look for a byte from serial
                if self.ser.in_waiting>0:
                    # data available from the serial port
                    lastchar=self.ser.read(1)

                    if lastchar==b'\xfe': #EOL
                        print("\nValue received")
                        self.useData()
                        self.inbuffer =[]
                    else:
                        # append
                        self.inbuffer.append (lastchar)

            # get from feed each 2 seconds

            ts = time.time()
            #wait 5 seconds (maybe less? 2) to avoid throttle on adafruit
            if ts - lasttime > 2:
                for i in range(2):
                    #feedname = 'sensors'
                    headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
                    url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME,feedname[i])
                #url0 = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME, feedname[0])
                #url1 = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME, feedname[1])
                    #url = "	https://io.adafruit.com/lawl/feeds/sensors"
                    #print(url)
                    myGET = requests.get(url, headers=headers)
                #myGET0 = requests.get(url0, headers=headers)
                #myGET1 = requests.get(url1, headers=headers)
                    #print(myGET.json())
                    responseJsonBody = myGET.json()
                #responseJsonBody0 = myGET0.json()
                #responseJsonBody1 = myGET1.json()
                    val[i] = responseJsonBody.get('value', None)
                #val[0] = responseJsonBody0.get('value', None)
                #val[1] = responseJsonBody1.get('value', None)
                    print(val)

                    if val[0] == '1':
                        self.ser.write(b'ON')

                    if val[0] == '0':
                        self.ser.write(b'OFF')

                    if val[1] == '2':
                        self.ser.write(b'W')
                    else:
                        self.ser.write(b'N')

                lasttime = time.time()


    def useData(self):
        # I have received a line from the serial port. I can use it
        if len(self.inbuffer)<3:   # at least header, size, footer
            return False
        # split parts
        if self.inbuffer[0] != b'\xff':
            return False

        #lasttime = time.time()
        numval = int.from_bytes(self.inbuffer[1], byteorder='little')
        #print(numval)
        val = ['0', '0']
        #print(val)

        feedname =['tempsensor','watsensor']
        #print(feedname)
        for i in range (numval):
        #if(numval > 1):
            #i = 0
            val[i] = int.from_bytes(self.inbuffer[i+2], byteorder='little')
            #strval = "Sensor %d: %d " % (i, val[i])
            #print(val)
            #print(strval)
            mypostdata = {'value': val[i]}
            #feedname = 'sensors'
            headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
            url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'.format(ADAFRUIT_IO_USERNAME, feedname[i])
            #url = 	"https://io.adafruit.com/lawl/feeds/sensors"
            #print(url)
            myPOST = requests.post(url, data=mypostdata, headers=headers)
            #print(myPOST.json())

        print(val)
            # get from feed each 5 seconds
            #ts = time.time
            #if ts - lasttime > 5:
            #feedname = 'sensors'
            #headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
            #url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME,feedname)
            #print(url)
            #myGET = requests.get(url, headers=headers)
            #responseJsonBody = myGET.json()
            #rec_val[i] = responseJsonBody.get('value', None)

            #print(rec_val[i])

            #if rec_val[0] == '1':
            #    self.ser.write(b'ON')

            #if rec_val[0] == '0':
            #    self.ser.write(b'OFF')

            #if rec_val[1] > '0':
            #    self.ser.write(b'W')

            #lasttime = time.time()

        #num = input("Enter: ")
        #self.ser.write(bytes(num, 'utf-8'))



if __name__ == '__main__':
    br=Bridge()
    br.setup()
    br.loop()



