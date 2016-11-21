from thingspeak import get_encode
from thingspeak import putThings
from thingspeak import getThings
from thingspeak import updateGraph

import serial
import time
import sched
import sys
import httplib, urllib

# configure the serial connections for BlueTooth dongle 
ser1 = serial.Serial(
                    #for mac
                    #port = '/dev/tty.usbmodem1411',
                    #for Pi
    port = '/dev/ttyACM' + str(sys.argv[1]),
	baudrate = 57600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS
)

"""ser2 = serial.Serial(
                    #for mac
                    #port = '/dev/tty.usbmodem1411',
                    #for Pi
    port = '/dev/ttyACM' + str(sys.argv[2]),
	baudrate = 115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS
)"""

ser1.close()
ser1.open()
#ser1.isOpen()

#ser2.close()
#ser2.open()

#filepointer = open('output.txt', 'w')
def putThings(pos,cmdStr, cmdID):
    params = urllib.urlencode({'position':pos,'command_string':cmdStr,'api_key':'R5EFGCTY8SAETNOY'})
    conn =httplib.HTTPConnection("api.thingspeak.com")
    conn.request("PUT","/talkbacks/984/commands/"+str(cmdID)+"?"+params)
    r1 = conn.getresponse()
    print "PUT: ", r1.status, r1.reason, r1.read()
    conn.close()
    return r1.status

def getThings(cmdID):
    conn =httplib.HTTPConnection("api.thingspeak.com")
    conn.request("GET","/talkbacks/984/commands/"+str(cmdID)+"?api_key=R5EFGCTY8SAETNOY")
    r1 = conn.getresponse()
    data = r1.read()
    print r1.status, r1.reason
    conn.close()
    return data
def updateGraph(f1,f2):
    params = urllib.urlencode({'field1': f1, 'field2': f2,'key':'VTU6OB7P4Y0DCJRO'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()

def get_encode():
    sin_freq = getThings(49011)
    sin_on = getThings(49012)
    d_IO = getThings(49024)
    ADC_freq = getThings(49025)
    cmd = int('0b0',2)
    #cmd += (sin_freq/10)
    line = ADC_freq+d_IO+sin_on+sin_freq
    #line = sin_freq+sin_on+d_IO+ADC_freq
    print "received: ", line
    cmd_chars = list(line)
    cmd = ord(cmd_chars[0])-48
    for i in range (1,6):
        print cmd_chars[i]
        cmd <<= 1
        cmd = cmd + ord(cmd_chars[i])-48
    print "binary: ", "{0:b}".format(cmd)
    print "commands: ", line
#   print " ".join(hex(cmd))
    return cmd

import struct

def collect_data(serial):
    adc_header = serial.read()
    assert(adc_header == 'a')
    adc_count_str = serial.read(4)
    adc_count = struct.unpack(">i", adc_count_str)[0]
    print "adc_count", adc_count
    adc_data = []
    for i in range(0, adc_count):
        adc_short_str = serial.read(2)
        adc_short = struct.unpack(">H", adc_short_str)[0]
        adc_data.append(adc_short)

    light_sensor_header = serial.read()
    assert(light_sensor_header == 'l')
    light_sensor_count_str = serial.read(4)
    light_sensor_count = struct.unpack(">i", light_sensor_count_str)[0]
    print "light_sensor_count", light_sensor_count
    light_sensor_data = []
    for i in range(0, light_sensor_count):
        light_sensor_short_str = serial.read(2)
        light_sensor_short = struct.unpack(">H", light_sensor_short_str)[0]
        light_sensor_data.append(light_sensor_short)

    timestamp_event_header = serial.read()
    assert(timestamp_event_header == 'd')
    timestamp_event_count_str = serial.read(4)
    timestamp_event_count = struct.unpack(">i", timestamp_event_count_str)[0]
    print "timestamp_event_count", timestamp_event_count
    timestamp_event_data = []
    for i in range(0, timestamp_event_count):
        timestamp_event_long_str = serial.read(8)
        timestamp_event_long = struct.unpack(">Q", timestamp_event_long_str)[0]
        timestamp_event_data.append(timestamp_event_long)

    print "adc_data", adc_data
    print "light_data", light_sensor_data
    print "timestamp_data", timestamp_event_data
    

while 1 :
    
    t1_us = int(round(time.time()*1000000))
    ser1.write('s')
    ser1.flush()

    t2_us = int(round(time.time()*1000000))
#    ser2.write('s')
#    ser2.flush()


    #TimeMMSS = time.strftime('%H:%M:%S', time.localtime(time1))
    #print(TimeMMSS)
    #time_ms = time1*1000%1000;
    #ser.write(TimeMMSS + ':' + str(time_ms) + '\n')
    t1_us_str = str(t1_us) + '\n'
    print "sending t1", t1_us_str
    ser1.write(t1_us_str)
    ser1.flush()
#    ser2.write(str(t2_us) + '\n')
#    ser2.flush()   #time.sleep(2)

    resp = ser1.read()
    t4_us = int(round(time.time()*1000000))
    t4_us_str = str(t4_us) + '\n'
    print "sending t4", t4_us_str
    ser1.write(t4_us_str)
    ser1.flush()
    
#    resp = ser2.read()
    t5_us = int(round(time.time()*1000000))
#    ser2.write(str(t5_us) + '\n')
#    ser2.flush()
    print "reading debug info"
    print "ser1", ser1.readline()
    print "ser1", ser1.readline()
    print "ser1", ser1.readline()
    print "ser1", ser1.readline()
#    print "ser2", ser2.readline()
#    print "ser2", ser2.readline()

#    cmd = getThings(49011)
#    if cmd == 'on': 
#       mbed_uart_ThingSpeak ser1.write('a')
#        ser2.write('a')
#    elif cmd == 'off':
#        ser1.write('b')
#        ser2.write('b')
#    else: 
#        ser1.write('c')
#        ser2.write('c')

    updateGraph(t4_us,t5_us)
    cmd = int('0b0',2)
    cmd = get_encode()
    ser1.write(chr(cmd))
    
#    ser2.write(cmd)

    # collect data here
    collect_data(ser1)
#    collect_data(ser2)

    time.sleep(2)

# Sine wave output Freq: 1/10/100/1000  command ID = 49011  position: 1
# Sine wave output On/Off               command ID = 49012  position: 2
# Digital I/O On/Off                    command ID = 49024  position: 3
# ADC Sampling Freq: 1/10/100/Off       command ID = 49025  position: 4


# sine wave output freq = 1HZ           x x x x 0 0
# sine wave output freq = 10HZ          x x x x 0 1
# sine wave output freq = 100HZ         x x x x 1 0
# sine wave output freq = 1kHZ          x x x x 1 1

# sine wave on/off      Off             x x x 0 x x
# sine wave on/off      ON              x x x 1 x x

# Digital output        Off             x x 0 x x x
# Digital output        On              x x 1 x x x

# ACD Sample OFF                        x 0 x x x x 
# ACD Sample rate freq = 1HZ            x 1 x x x x 
# ACD Sample rate freq = 10HZ           1 0 x x x x
# ACD Sample rate freq = 100HZ          1 1 x x x x 
