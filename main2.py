#!/usr/bin/env python

import i2c_driver
import time
import schedule
from pydub import AudioSegment
from pydub.playback import play
import RPi.GPIO as GPIO
import threading
import sys 
from multiprocessing import Process
import subprocess
from playsound import playsound
import random 

# Seting GPIO modes 
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)


mylcd = i2c_driver.LCD()

def mainLoop():
    alarmSet = False
    
    # Cleaning screen at beggining     
    cleanDisplay()
    while alarmSet == False:
        channel = GPIO.wait_for_edge(17, GPIO.BOTH, timeout=1000)
        if channel is None:            
            mylcd.lcd_display_string(time.strftime('%I:%M:%S %p'), 1)
            mylcd.lcd_display_string(time.strftime('%a %b %d, 20%y'), 2)
        else:
            cleanDisplay()
            # Getting hour and minute from user 
            hour = setHour()
            minute = setMinutes()
            
            # Setting time 
            alarmSet, alarmTime = checkHour(hour, minute)
            if alarmSet == True:
                schedule.every().day.at(alarmTime).do(job)
                
                # Printing allert
                cleanDisplay()
                mylcd.lcd_display_string(('Alarm set to:'), 1)
                mylcd.lcd_display_string(alarmTime, 2)
                time.sleep(1);
            cleanDisplay()
            

    while alarmSet == True:  
        schedule.run_pending()
        time.sleep(1)
        mylcd.lcd_display_string(time.strftime('%I:%M:%S %p'), 1)
        mylcd.lcd_display_string(time.strftime('%a %b %d, 20%y'), 2)

# Cleaning display 
def cleanDisplay():
    mylcd.lcd_display_string("                ", 1)
    mylcd.lcd_display_string("                ", 2)
    
# Setting hour by hitting     
def setHour():
    timeForSetingHour = 30
    hour = 0

    cleanDisplay()
    mylcd.lcd_display_string('Set your hour:', 1)
    mylcd.lcd_display_string(str(hour), 2)
            
    while 0 < timeForSetingHour:
        channel = GPIO.wait_for_edge(17, GPIO.BOTH, timeout=1000)
        if channel is None:            
            timeForSetingHour -= 1
        else:          
            timeForSetingHour -= 1
            hour += 1 
            mylcd.lcd_display_string('Set your hour:', 1)
            mylcd.lcd_display_string(str(hour), 2)

    return hour 
    
# Setting minutes by hitting  
def setMinutes():
    timeForSetingMinutes = 60
    minute = 0

    cleanDisplay()
    mylcd.lcd_display_string('Set your minute:', 1)
    mylcd.lcd_display_string(str(minute), 2)
        
    while 0 < timeForSetingMinutes:
        channel = GPIO.wait_for_edge(17, GPIO.BOTH, timeout=1000)
        if channel is None:            
            timeForSetingMinutes -= 1
        else:          
            timeForSetingMinutes -= 1
            minute += 1 
            mylcd.lcd_display_string('Set your minutes:', 1)
            mylcd.lcd_display_string(str(minute), 2)

            
    return minute

# Scheduled job 
def job():
    # Define how many times we should hit sensor to turn off the alarm 
    hitTarget = random.randrange(5, 10)
    
    cleanDisplay()
    mylcd.lcd_display_string("Hit me:", 1)
    mylcd.lcd_display_string(str(hitTarget) + " times", 2)
    
    # Playing asynch sound 
    playsound('kanye_alarm.wav', False)
    count = 0
    while count < hitTarget:
        channel = GPIO.wait_for_edge(17, GPIO.BOTH, timeout=1000)
        if channel is None:            
            continue
        else:
            hitTarget -= 1
            mylcd.lcd_display_string(str(hitTarget) + " times", 2)
        
        
    #mylcd.lcd_display_string("You wake up?:", 1)
    #mylcd.lcd_display_string("1-nap|0-no nap", 2)
    
    cleanDisplay()
    mylcd.lcd_display_string("Thanks for" , 1)
    mylcd.lcd_display_string("using!", 2)
    sys.exit()
    
def checkHour(hour, minute):
    if 0 <= hour <= 23 and 0 <= minute <= 59:
        if hour < 10:
            textHour = '0' + str(hour)
        else:
            textHour = str(hour)
        if minute < 10:
            textMinute = '0' + str(minute)
        else:
            textMinute = str(minute)
        print("Returning true")
        return True, textHour + ':' + textMinute
    else:
        print("Returning false")
        return False, "false"
    
    

mainLoop()
    