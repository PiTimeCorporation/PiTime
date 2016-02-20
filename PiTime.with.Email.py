#Import all the modules that are needed

import time

import RPi.GPIO as GPIO

import picamera

import math

from math import floor

import smtplib




#The pin which receives the input from the motion sensor is pin 4

sensor = 4




#Set up the GPIO for interface with the motion sensor

GPIO.setmode(GPIO.BCM)

GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)




#Set up the PiCamera

camera = picamera.PiCamera()




print("PiTime is an automated timing device for use in sporting competition and training, and comes equipped with photofinish and an inbuilt emailing function to send the results to those in charge of producing the results.")      




#Get the user's details for the email sending function

senderaddress = "pitimecorporation@hotmail.com"

password = "RaspberryPi"

receiveraddress = input("\nWhat is the email address of the recipient? ")




#Start the system (including the timer) when the gun goes

starting_gun = input("\nWaiting for the gun") 

starttime = time.time()




print("\nYou can stop the program by pressing Ctrl+C")




#This will be the content of the email which contains the provisional results

content = ""




position = 0

#The main part of the program; collecting the times and taking the pictures when

#the athletes cross the line, and saving these jpeg files as their finishing

#time

try:

    while True:

        if GPIO.input(sensor):

            finishtime = time.time()

            if finishtime - starttime < 10:

                result = round(finishtime - starttime, 4)

            elif finishtime - starttime < 60:

                result = round(finishtime - starttime, 5)

            elif finishtime - starttime < 3600:

                result = round((floor((finishtime - starttime)/60) + ((finishtime - starttime)%60)/100), 6) 

            else:

                result = round((floor((finishtime - starttime)/60) + ((finishtime - starttime)%60)/100), 7) 

            position += 1

            ordinal = position, ": "

            print(position, ": ", result)

            content += str(ordinal)+str(result)+"\n"

            camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))

            camera.capture(str(result)+".jpg")

            camera.stop_preview()

except KeyboardInterrupt:

    pass




#Send the provisional results by email from the user's email address to the

#person in charge of the results

print("\nNow sending results via email...")

mail = smtplib.SMTP("smtp.live.com",25)

mail.ehlo()

mail.starttls()

mail.login(senderaddress,password)

mail.sendmail(senderaddress,receiveraddress,content)

mail.close

print("Results sent.")




#Allow the user to exit the program cleanly

input("\nPress enter to exit the program")
