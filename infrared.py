import RPi.GPIO as GPIO
import time

INFRA = 22
TRIG = 27
ECHO = 18 
BUZZ = 17
BUTT = 5

CM = [0, 262, 294, 330, 350, 393, 441, 495]


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(INFRA, GPIO.IN)
    GPIO.setup(BUZZ, GPIO.OUT)
    GPIO.setup(BUTT, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set Button's mode as input, and pull up to high level(3.3V)
    global buzz
    buzz = GPIO.PWM(BUZZ,440)
    buzz.start(10) 
    GPIO.add_event_detect(BUTT, GPIO.BOTH, callback=detect, bouncetime=200)


def detect(chn):
    Led(GPIO.input(BtnPin))


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


def program(): 
    while True:
        if GPIO.input(INFRA):
            print('I SAW SOMETHING')
            dis = distance()
            print(dis, 'cm')
            if (dis < 100):
                buzz.ChangeFrequency(CM[6])
            elif (dis < 200):
                buzz.ChangeFrequency(CM[4])
            elif (dis < 300):
                buzz.ChangeFrequency(CM[2])
            else:
                buzz.ChangeFrequency(200)
        else:
            print('No motion')
            buzz.ChangeFrequency(10)
        time.sleep(0.3)    

def destroy():
    GPIO.cleanup()


if __name__ == "__main__": 
	setup()
	print('Starting Up!')
	try:
		program()	
	except KeyboardInterrupt:
		destroy()	
