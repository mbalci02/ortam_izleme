import RPi.GPIO as GPIO
import sys
import time
import datetime
import Adafruit_DHT
import spidev
import os
import MySQLdb
import smtplib
from mq import *

conn = MySQLdb.connect(user="root",
                  passwd="********",
                  db="Ortam_Izleme")
x = conn.cursor()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(7,GPIO.IN)           #Alev Sensoru
GPIO.setup(26, GPIO.IN)         #Hareket Sensoru
GPIO.setup(13, GPIO.IN)		#Sivi sensoru
GPIO_TRIGGER = 18		#Mesafe Sensoru
GPIO_ECHO = 24			#Mesafe Sensoru
 
#set GPIO direction (IN / OUT)	    
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  #Mesafe Sensoru
GPIO.setup(GPIO_ECHO, GPIO.IN)	    #Mesafe Sensoru

# Open SPI bus LDR icin
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

def ReadChannel(channel): 		#LDR icin
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def ConvertVolts(data,places):		#LDR icin
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts

def ConvertTemp(data,places):		#LDR icin
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp

light_channel = 1

input = GPIO.input(7)           #Alev Sensoru
sensor=Adafruit_DHT.DHT11
gpio=14

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def mailgonder(message):
    fromaddr = '******@gmail.com'  
    toaddrs  = '*******@windowslive.com'  

    username = '*********@gmail.com'  
    password = '*********'

    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.ehlo()
    server.starttls()
    server.login(username, password)  
    server.sendmail(fromaddr, toaddrs, message)  
    server.quit()

zaman= time.strftime("Zaman: %d/%m/%Y %H:%M:%S")
mq = MQ();
sayac=0
i=GPIO.input(26)              #Hareket sensoru icin
k=GPIO.input(13)	

while True:
  	#Sivi sensoru icin
  dist = distance()     #Mesafe icin
  
  konu='ORTAM IZLEME ALARM!'
  
  light_level = ReadChannel(light_channel)
  light_volts = ConvertVolts(light_level,2)
 
  # Print out results
  print "----------------------------------------------------------"
  print time.strftime("Zaman: %d/%m/%Y %H:%M:%S") 
  print("Parlaklik: {} LUX ({}V)".format((1023-light_level),light_volts))
  lux=1023-light_level
  
  perc = mq.MQPercentage()
  sys.stdout.write("\r")
  sys.stdout.write("\033[K")
  sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
 
  humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
  print('\nSicaklik={0:0.1f}*C  Nem={1:0.1f}%'.format(temperature, humidity))
  print "----------------------------------------------------------"
  print ("Olculen Yukseklik = %.1f cm" %((59.3)-dist))
  
  seviye=(59.3)-dist
  
  LPG=perc["GAS_LPG"]
  KARBMNKST=perc["CO"]
  DUMAN=perc["SMOKE"]
  
#  if (GPIO.input(7))==1:		#Alev kontrolu
   #mesaj=('ORTAMDA ALEV TESPIT EDILDI!...\nSicaklik={0:0.1f}*C  Nem={1:0.1f}%'.format(temperature, humidity))
   #mailgonder(message = 'Subject: {konu}\n\n{mesaj}'.format(konu=konu,mesaj=mesaj))
 #  print("Alev tespit edildi!")
  # x.execute("INSERT INTO Kayitli_Olcumler(ZAMAN2,ZAMAN,SICAKLIK,NEM,SIVI_SEVIYE,PARLAKLIK,CO,LPG,DUMAN,DURUM) \
   #VALUES (UNIX_TIMESTAMP(NOW()),NOW(),%s,%s,%s,%s,%s,%s,%s,'ALEV TESPIT EDILDI!')",(format(temperature),format(humidity),seviye,lux,perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))

  if i==1:               	#Hareket kontrolu
   mesaj='ORTAMDA HAREKET TESPIT EDILDI!...'
   mailgonder(message = 'Subject: {konu}\n\n{mesaj}'.format(konu=konu,mesaj=mesaj))
   print "\nHareket Var!..",i
   x.execute("INSERT INTO Kayitli_Olcumler(ZAMAN2,ZAMAN,SICAKLIK,NEM,SIVI_SEVIYE,PARLAKLIK,CO,LPG,DUMAN,DURUM) \
   VALUES (UNIX_TIMESTAMP(NOW()),NOW(),%s,%s,%s,%s,%s,%s,%s,'HAREKET TESPIT EDILDI!')",(format(temperature),format(humidity),seviye,lux,perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))

  elif k==1 and seviye>(7.0):               	#Sivi kontrolu
   print "\nSivi Temasi Var!..",k
   mesaj='ORTAMDA SIVI TESPIT EDILDI!...'
   mailgonder(message = 'Subject: {konu}\n\n{mesaj}'.format(konu=konu,mesaj=mesaj))
   x.execute("INSERT INTO Kayitli_Olcumler(ZAMAN2,ZAMAN,SICAKLIK,NEM,SIVI_SEVIYE,PARLAKLIK,CO,LPG,DUMAN,DURUM) \
   VALUES (UNIX_TIMESTAMP(NOW()),NOW(),%s,%s,%s,%s,%s,%s,%s,'SIVI TESPIT EDILDI!')",(format(temperature),format(humidity),seviye,lux,perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))

  elif float(LPG)>(5.0) or float(KARBMNKST)>(5.0) or float(DUMAN)>(5.0):       #Gaz Kontrolu
   print("\nLPG=%g ppm  CO=%g ppm DUMAN=%g ppm" %(perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
   print('\nSicaklik={0:0.1f}*C  Nem={1:0.1f}%'.format(temperature, humidity))
   mesaj='ORTAMDAKI GAZ NORMALIN USTUNDE!...'
   mailgonder(message = 'Subject: {konu}\n\n{mesaj}'.format(konu=konu,mesaj=mesaj))
   x.execute("INSERT INTO Kayitli_Olcumler(ZAMAN2,ZAMAN,SICAKLIK,NEM,SIVI_SEVIYE,PARLAKLIK,CO,LPG,DUMAN,DURUM) \
   VALUES (UNIX_TIMESTAMP(NOW()),NOW(),%s,%s,%s,%s,%s,%s,%s,'ORTAMDAKI GAZ NORMALIN USTUNDE!')",(format(temperature),format(humidity),seviye,lux,perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))

  elif float(format(temperature))>(48.0):       #Sicaklik Kontrolu
   mesaj=("ORTAMDAKI SICAKLIK NORMALIN USTUNDE!...\nSicaklik={0:0.1f}*C  Nem={1:0.1f}% ".format(temperature,humidity))
   mailgonder(message = 'Subject: {konu}\n\n{mesaj}'.format(konu=konu,mesaj=mesaj))
   x.execute("INSERT INTO Kayitli_Olcumler(ZAMAN2,ZAMAN,SICAKLIK,NEM,SIVI_SEVIYE,PARLAKLIK,CO,LPG,DUMAN,DURUM) \
   VALUES (UNIX_TIMESTAMP(NOW()),NOW(),%s,%s,%s,%s,%s,%s,%s,'ORTAMDAKI SICAKLIK NORMALIN USTUNDE!')",
   (format(temperature),format(humidity),seviye,lux,perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
      
  elif sayac==90:
   print("15 dakika gecti!\n")
   x.execute("INSERT INTO Kayitli_Olcumler(ZAMAN2,ZAMAN,SICAKLIK,NEM,SIVI_SEVIYE,PARLAKLIK,CO,LPG,DUMAN,DURUM) \
   VALUES (UNIX_TIMESTAMP(NOW()),NOW(),%s,%s,%s,%s,%s,%s,%s,'ORTAM NORMAL!')",(format(temperature),format(humidity),seviye,lux,perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
   sayac=0
  
  else:
   sayac=sayac+1
   print("\nOrtamda Problem Yok!..")
   x.execute("INSERT INTO Anlik_Olcumler(ZAMAN2,ZAMAN,SICAKLIK,NEM,SIVI_SEVIYE,PARLAKLIK,CO,LPG,DUMAN,DURUM) \
   VALUES (UNIX_TIMESTAMP(NOW()),NOW(),%s,%s,%s,%s,%s,%s,%s,'ORTAM NORMAL!')",(format(temperature),format(humidity),seviye,lux,perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
   conn.commit()
   time.sleep(10)
