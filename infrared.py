import RPi.GPIO as GPIO
import time


# GPIO Pin locations of each sensor
INFRA = 22
TRIG = 27
ECHO = 18 
BUZZ = 17
BUTT = 5
# Set Button initial value to True
pushed = True
# Array of frequencies for buzzer
CM = [0, 262, 294, 330, 350, 393, 441, 495]


# Initial setup of everything
def setup():
    print('Starting Up!')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(INFRA, GPIO.IN)      # Setup infrared sensor is an input
    GPIO.setup(BUZZ, GPIO.OUT)      # Setup buzzer as output
    GPIO.setup(BUTT, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set Button's mode as input, and pull up to high level(3.3V)
    global buzz                     # Define buzzer as a global variable
    buzz = GPIO.PWM(BUZZ,440)
    GPIO.add_event_detect(BUTT, GPIO.RISING, callback=detect, bouncetime=200)
    for i in range(5):
        buzz.start(10)       # Start buzz at 10Hz frequency upon startup
        time.sleep(0.33)
        buzz.stop()
        time.sleep(0.66)     # Sleep for 5 seconds so that sensors can start up properly


# Check if button has been pressed
def detect(channel):
    global pushed         # Make the button push a global variable
    print('BUTTON PUSHED')
    # Switch False to True or True to False
    pushed = not pushed


# Check distance from ultrasonic sensor
def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)


    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100


# Infrared input saw something
def motion():
    print('I SAW SOMETHING!!!')
    dis = distance()              # Take initial distance from ultrasonic input
    buzz.start(10)                # Turn on buzzer at 10Hz
    while (pushed and dis < 1200):           # If distance > 1200 cm, turn off sensors, person gone
        dis = distance()          # Calculate distance at each instance of while loop
        print(round(dis, 2), 'cm')  # Display distance rounded to 2 decimal places
        if (dis < 100):           # If 0 < distance < 100, play highest frequency
            buzz.ChangeFrequency(CM[6])
        elif (dis < 200):         # If 100 < distance < 200, play next highest frequency
            buzz.ChangeFrequency(CM[4])
        elif (dis < 300):         # If 200 < distance < 300, play third highest frequency
            buzz.ChangeFrequency(CM[2])
        else:                     # If 300 < distance < 1200, play lowest frequency
            buzz.ChangeFrequency(200)
        time.sleep(0.33)           # Calculate change 3 times per second
    if not pushed:
        buzz.stop()               # Turn off buzzer if button set to off


# No motion detected, turn off buzzer
def noMotion():
    print('No motion')
    buzz.stop()     # Turn off buzzer   
    

# If infrared sensor detects person, start buzzing as defined in motion function
# If infrared sensor doesn't detect person and motion loop isn't running, turn off
def program():
    while True:
        while pushed:
            motion() if GPIO.input(INFRA) else noMotion()
            time.sleep(0.33)   # Check this 3 times per second   


# KeyboardInterrupt, turn off buzzer and clean up
def destroy():
    buzz.stop()       # Turn off Buzzer
    GPIO.cleanup()    # Release resource


# MAIN
# Calls all functions in necessary order
if __name__ == '__main__':
    setup()
    try: program()
    except KeyboardInterrupt: destroy()