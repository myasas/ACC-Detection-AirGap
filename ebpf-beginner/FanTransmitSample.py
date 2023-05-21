import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(14, IO.OUT)
fan = IO.PWM(14, 100)
fan.start(0)

message = "ABCDEF"  # The hidden message to send
speed_levels = {
    'A': 15,
    'B': 30,
    'C': 45,
    'D': 60,
    'E': 75,
    'F': 90
}

def send_message(character):
    # Implement code to send the character to the receiver
    # This could involve using a wireless module (e.g., Wi-Fi, Bluetooth) or other communication protocols
    
    # Placeholder code to print the character for demonstration purposes
    print("Sending character:", character)

for character in message:
    if character in speed_levels:
        fan_speed = speed_levels[character]
        fan.ChangeDutyCycle(fan_speed)
        send_message(character)
        time.sleep(5)  # Adjust the delay as needed
    else:
        print("Invalid character:", character)

fan.stop()
IO.cleanup()
