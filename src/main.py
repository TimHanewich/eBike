import machine
import throttle
import time

# set up throttle
t = throttle.Throttle(26)

# set up motor PWM output
pwm = machine.PWM(machine.Pin(0))
pwm.freq(50)
pwm.duty_u16(0) # start at 0

while True:

    # read input from throttle
    throttle_percent:float = t.read()

    # apply a governor to the throttle
    governor:float = 0.5 # cut to X% power
    throttle_percent = throttle_percent * governor

    # calcualte what duty cycle to enact, in nanoseconds
    # the standards for PWM motor input:
    # 1,000,000 nanoseconds = 1ms = the minimum throttle
    # 2,000,000 nanoseconds = 2ms = the maximum throttle
    duty_ns:int = 1000000 + int(throttle_percent * 1000000)
    duty_ns = min(max(duty_ns, 2000000), 1000000)

    # print?
    print("Throttle Input = " + str(int(throttle_percent * 100)) + "%, duty in nanoseconds = " + str(duty_ns))

    # apply
    pwm.duty_ns(duty_ns)

    # wait
    time.sleep(0.1)