#Name = Sandip Thapa, Sarun Shrestha, Yechan Kim
#Date = 15 November 2023
#Description = RPi 4 Simon


import RPi.GPIO as GPIO
from time import sleep
from random import randint
import pygame

# set to True to enable debugging output
DEBUG = False

# initialize the pygame library
pygame.init()

# set the GPIO pin numbers
# the switches (from L to R)
switches = [ 20, 16, 12, 26 ]

# the LEDs (from L to R)
leds = [6, 13, 19, 21 ]

# the sounds that map to each LED (from L to R)
sounds = [ pygame.mixer.Sound("one.wav"),
           pygame.mixer.Sound("two.wav"),
           pygame.mixer.Sound("three.wav"),
           pygame.mixer.Sound("four.wav") ]

# use the Broadcom pin mode
GPIO.setmode(GPIO.BCM)

# setup the input and output pins
GPIO.setup(switches, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leds, GPIO.OUT)

# this function turns the LEDs on
def all_on():
    for i in leds:
        GPIO.output(leds, True)

# this function turns the LEDs off
def all_off():
 for i in leds:
     GPIO.output(leds, False)

# this functions flashes the LEDs a few times when the player loses the game
def lose(sequence_length):
    score = sequence_length
    
    if score == 0:
        print(f"You made it to a sequence of {score}!")

    for i in range(0, 4):
        all_on()
        sleep(0.5)
        all_off()
        sleep(0.5)

#Function to turn on LED and turn off LED
def turn_on_led(led):
             GPIO.output(leds[s], True)

def turn_off_led(led):
             GPIO.output(leds[s], False)        

# the main part of the program
# initialize the Simon sequence # each item in the sequence represents an LED (or switch),indexed at 0 through 3
seq = []


# randomly add the first two items to the sequence
seq.append(randint(0, 3))
seq.append(randint(0, 3))

print("Welcome to Simon!")
print("Try to play the sequence back by pressing the switches.")
print("Press Ctrl+C to exit...")

# we'll discuss this later, but this allows us to detect
# when Ctrl+C is pressed so that we can reset the GPIO pins 
try:
    # keep going until the user presses Ctrl+C
    while (True):
    # randomly add one more item to the sequence
        seq.append(randint(0, 3))
        if (DEBUG):
            # display the sequence to the console
            if (len(seq) > 3):
                print()
            print("seq={}".format(seq))
        # display the sequence using the LEDs
        for s in seq:
             # function to turn the appropriate LED on
             GPIO.output(leds[s], True)
             # play its corresponding sound
             sounds[s].play()
             # wait and turn the LED off again
             sleep(1)
             GPIO.output(leds[s], False)
             sleep(0.5)


        # Over time, increase the speed of the playing sequence.

        if len(seq) >= 5:
            play_time = 0.9
            delay_time = 0.4
        if len(seq) >= 7:
            play_time = 0.8
            delay_time = 0.3
        if len(seq) >= 10:
            play_time = 0.7
            delay_time = 0.25
        if len(seq) >= 13:
            play_time = 0.6
            delay_time = 0.15

        if len(seq) <= 15:

            # Playing the sequence with LED control
            for music in seq:
                # Turn on the LED
                turn_on_led(leds[music])

                # Play the sound
                sounds[music].play()

                # Delay the play time
                sleep(play_time)

                # Turn off the LED
                turn_off_led(leds[music])

                # Delay between notes
                sleep(delay_time)
        else:
            # Play the sequence without LEDs control, only audibly
            for music in seq:
                # Play the sound
                sounds[music].play()

                # Delay between notes
                sleep(play_time)

                # Delay between notes
                sleep(delay_time)

        # wait for player input (via the switches)
        # initialize the count of switches pressed to 0
        switch_count = 0

        # keep accepting player input until the number of items in the sequence is reached
        while (switch_count < len(seq)):

            # initially note that no switch is pressed
            # this will help with switch debouncing
            pressed = False

            # so long as no switch is currently pressed...
            while not pressed:

                # ...we can check the status of eachswitch
                for i in range(len(switches)):

                    # if one switch is pressed
                    while (GPIO.input(switches[i]) == True):

                        # note its index
                        val = i

                        # note that a switch has now been pressed
                        # so that we don't detect any more switch presses
                        pressed = True
        if DEBUG:
             # display the index of the switch pressed
             print(val,end =",")

        # light the matching LED when using LED
        GPIO.output(leds[val], True)

        # play its corresponding sound
        sounds[val].play()

        # wait and turn the LED off again
        sleep(1)
        GPIO.output(leds[val], False)
        sleep(0.25)

        # check to see if this LED is correct in the sequence
        if val != seq[switch_count]:

            # player is incorrect; invoke the lose function
            lose(switch_count)

            # reset the GPIO pins
            GPIO.cleanup()

            # exit the game
            exit(0)

        # if the player has this item in the sequence correct, increment the count
        switch_count += 1

# detect Ctrl+C 
except KeyboardInterrupt:

    # reset the GPIO pins

    GPIO.cleanup()
