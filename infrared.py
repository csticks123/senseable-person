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
    GPIO.setup(INFRA, GPIO.IN)  # Setup infrared sensor is an input
    GPIO.setup(BUZZ, GPIO.OUT)  # Setup buzzer as output
    # Set Button's mode as input, and pull up to high level(3.3V)
    GPIO.setup(BUTT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global buzz                 # Define buzzer as a global variable
    buzz = GPIO.PWM(BUZZ,440)
    GPIO.add_event_detect(BUTT, GPIO.RISING, callback=detect, bouncetime=200)
    for i in range(5):
        buzz.start(100)      # Start buzz to play startup tone
        time.sleep(0.33)
        buzz.stop()
        time.sleep(0.66)     # Sleep for 5 seconds so that sensors can start up properly


# Check if button has been pressed
def detect(channel):
    global pushed         # Make the button push a global variable
    print('BUTTON PUSHED')
    pushed = not pushed   # Switch false to true or true to false


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
    # Returns distance in inches
    return during * 340 / 5.08 * 100


# Infrared input saw something
def motion():
    print('I SAW SOMETHING!!!')
    dis = distance()        # Take initial distance from ultrasonic input
    buzz.start(10)          # Turn on buzzer
    # If distance > 10 ft, turn off sensors, person gone
    while (pushed and dis < 120):
        dis = distance()    # Calculate distance at each instance of while loop
        # Display distance in feet and inches (rounded to 2 decimal places)
        print(int(dis / 12), 'ft,', round(dis % 12, 2), 'in')
        if (dis < 12):      # If 0 ft < distance < 1 ft, play highest frequency
            buzz.ChangeFrequency(CM[7])    
        elif (dis < 24):    # If 1 ft < distance < 2 ft, play next highest frequency
            buzz.ChangeFrequency(CM[6])
        elif (dis < 36):    # If 2 ft < distance < 3 ft, play third highest frequency
            buzz.ChangeFrequency(CM[5])
        elif (dis < 48):    # If 3 ft < distance < 4 ft, play fourth highest frequency
            buzz.ChangeFrequency(CM[4])
        elif (dis < 60):    # If 4 ft < distance < 5 ft, play fifth highest frequency
            buzz.ChangeFrequency(CM[3])
        elif (dis < 72):    # If 5 ft < distance < 6 ft, play sixth highest frequency
            buzz.ChangeFrequency(CM[2])
        elif (dis < 84):    # If 6 ft < distance < 7 ft, play sixth highest frequency
            buzz.ChangeFrequency(CM[1])
        else:               # If 7 ft < distance < 10 ft, play lowest frequency
            buzz.ChangeFrequency(200)
        time.sleep(0.33)    # Calculate change 3 times per second
    if not pushed: buzz.stop()         # Turn off buzzer if button set to off


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