from machine import Pin, PWM
from time import sleep

# Setup the PWM for CO2 Laser
# For 48-1KAM we need a constant 1us Tickle. Then the duty defines power from there.
pwm = PWM(Pin(15))

freq=5000
tickle_ns=1000 #.5% is the tickle preionization PWM percentage
pwm.init(freq=freq, duty_ns=tickle_ns)

def get_ns(percent): # Function to convert percentage return corresponding nanosecond value.
    if not 0 < percent <= 100:
        return tickle_ns
    tickle_duty = percent*2000  # Convert percentage input into desired nanosecond value within the calculated period range by scaling it with respect to maximum possible duty cycle which is equal half of total time duration or one complete pulse width (5µs in this case).
    return tickle_duty   # Return corresponding nanosecond equivalent as output

sleep(2) #Give us time to get on serial...

print("It is safe to power on the laser!")

while True:
    try:
        percent = input("Enter Power Level in percent, or \"off\": ")
    except:
        sleep(5)
        continue
    if percent=="off" or percent == "Off":
        pwm.duty_ns(tickle_ns)
        print("Laser is in tickle precharge mode, it is safe to power off.")
        continue
    try:
        percent = int(float(percent))
        pwm.duty_ns(get_ns(percent))
    except:
        print("You must enter an integer percentage between 1 and 100")
        pwm.duty_ns(tickle_ns) # Rather than leave the laser on, lets turn it off to be safe!    
    
    #for duty in range(65025):
    #    pwm.duty_u16(duty)
    #    sleep(0.0001)
    #for duty in range(65025, 0, -1):
    #    pwm.duty_u16(duty)
    #    sleep(0.0001)