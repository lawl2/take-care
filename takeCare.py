import serial
import serial.tools.list_ports
import time
import requests

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat, bot
from config import BOTKEY, chatID
from threading import Timer,Thread,Event

import cv2
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

from random import uniform

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


#serial port used by Arduino
PORTNAME='COM5'


ADAFRUIT_IO_USERNAME = "name_to_use"
ADAFRUIT_IO_KEY = "key_to_use"

#initial sensors' value
val = ['0', '0']


#temperature limit to telegram
temp = 0


                            #######         KMeans algorithm            #######


class DominantColors:
    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None


    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image


    def dominantColors(self):
        # read image
        img = cv2.imread(self.IMAGE)

        # convert to rgb from bgr  (cv2 invert rgb colors)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))

        # save image after operations
        self.IMAGE = img

        # using k-means to cluster pixels
        kmeans = KMeans(n_clusters=self.CLUSTERS)
        kmeans.fit(img)

        # the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        # save labels
        self.LABELS = kmeans.labels_

        # returning after converting to integer from float
        return self.COLORS.astype(int)


    def plotHistogram(self):
        # labels form 0 to no. of clusters
        numLabels = np.arange(0, self.CLUSTERS + 1)

        # create frequency count tables
        (hist, _) = np.histogram(self.LABELS, bins=numLabels)
        hist = hist.astype("float")
        hist /= hist.sum()

        # appending frequencies to cluster centers
        colors = self.COLORS

        # descending order sorting as per frequency count
        colors = colors[(-hist).argsort()]
        hist = hist[(-hist).argsort()]

        # creating empty chart
        chart = np.zeros((50, 500, 3), np.uint8)
        start = 0

        # creating color rectangles
        for i in range(self.CLUSTERS):
            end = start + hist[i] * 500

            # getting rgb values
            r = colors[i][0]
            g = colors[i][1]
            b = colors[i][2]

            # using cv2.rectangle to plot colors
            cv2.rectangle(chart, (int(start), 0), (int(end), 50), (r, g, b), -1)
            start = end

        # display chart
        plt.figure()
        plt.axis("off")
        plt.imshow(chart)
        plt.show()


                            #######           Telegram BOT            #######


def startBot():
    global updater
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True
    updater = Updater(BOTKEY, use_context=True)

    # Get the dispatcher to register handlers  (callbacks)
    dp = updater.dispatcher


    # Start the Bot (polling of messages)
    # this call is non-blocking
    updater.start_polling()

    return updater



class perpetualTimer():

    # perpetual timer for sending messages
    def __init__(self, t, hFunction, param,val):
        self.t = t
        self.hFunction = hFunction
        self.param = param
        self.val = val
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction(self.param, self.val)
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()
        self.thread.cancel()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


def sendBotVal(updater,val):
    #sending values to the bot
    if(int(val[0]) > temp):
        #temperature to high
        updater.bot.send_message(chat_id=chatID, text='HIGH TEMPERATURE : ' + str(val[0]))
    if(int(val[1]) > 10):
        #loss problems
        updater.bot.send_message(chat_id=chatID, text='LOSS WARNING')


            #######           Bridge receiving/sending from/to Arduino and receiving/sending from/to the server           #######


class Bridge():

    def setupSerial(self):
        # control and open serial port
        self.ser = None
        print("list of available ports: ")

        ports = serial.tools.list_ports.comports()
        self.portname = None
        self.portname = PORTNAME
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

        self.ser.open()

        # internal input buffer from serial
        self.inbuffer = []


    def setup(self):
        self.setupSerial()

    def loop(self,updater):

        #infinite loop

        #sensors' feedname
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


            ts = time.time()
            #wait 2s
            if ts - lasttime > 2:
                for i in range(2):

                    #receiving data from server
                    headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
                    url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data/last'.format(ADAFRUIT_IO_USERNAME,feedname[i])
                    #print(url)

                    myGET = requests.get(url, headers=headers)
                    #print(myGET.json())
                    responseJsonBody = myGET.json()

                    val[i] = responseJsonBody.get('value', None)

                    #print(val)

                    #controlling and sending values to arduino
                    if val[0] == '1':
                        self.ser.write(b'ON')

                    if val[0] == '0':
                        self.ser.write(b'OFF')

                    if val[1] == '2':
                        self.ser.write(b'W')
                        
                    if val[1] == '0' or val[1] == '1':
                        self.ser.write(b'N')

                lasttime = time.time()



    def useData(self):
        #using data from serial port
        if len(self.inbuffer)<3:   # at least header, size, footer
            return False
        # split parts
        if self.inbuffer[0] != b'\xff':
            return False

        numval = int.from_bytes(self.inbuffer[1], byteorder='little')

        feedname =['tempsensor','watsensor']


        for i in range (numval):

            val[i] = int.from_bytes(self.inbuffer[i+2], byteorder='little')

            mypostdata = {'value': val[i]}

            headers = {'X-AIO-Key': ADAFRUIT_IO_KEY}
            url = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'.format(ADAFRUIT_IO_USERNAME, feedname[i])
            #print(url)

            myPOST = requests.post(url, data=mypostdata, headers=headers)
            #print(myPOST.json())

        print(val)

        #sending values to bot telegram
        if (int(val[0]) > temp or int(val[1]) > 10):

            # start thread
            randomizer = perpetualTimer(5, sendBotVal, updater, val)

            randomizer.start()




if __name__ == '__main__':

    # KMeans for classification
    img = r'C:\Users\Rocco\Documents\MAGISTRALE UNIMORE\I ANNO\IOTand3DIntelligentSystems\1.IOT\VGG samples-20210119\sang.jpg'
    clusters = 3
    dc = DominantColors(img, clusters)
    colors = dc.dominantColors()
    print(colors)
    dc.plotHistogram()

    for i in range(3):
        # red = blood
        if colors[i][0] > 200 and colors[i][1] < 50 and colors[i][2] < 50:
            temp = 6
            print("Blood")
            break
        # green = vaccines
        if colors[i][0] < 50 and colors[i][1] > 200 and colors[i][2] < 100:
            temp = 8
            print("Vaccines")
            break
        # blue = organs
        if colors[i][0] < 50 and colors[i][1] < 200 and colors[i][2] > 200:
            temp = 4
            print("Organs")
            break
    if (temp == 0):
        print("There's no mark. Impossibile to classificate")

    print(temp)

    br=Bridge()
    br.setup()


    # start bot
    updater = startBot()
    br.loop(updater)


