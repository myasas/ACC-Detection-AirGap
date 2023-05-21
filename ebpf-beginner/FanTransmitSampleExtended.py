import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(14, IO.OUT)
fan = IO.PWM(14, 100)
fan.start(0)

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA7Tyi7reA5lEABmbPhDOEKsuc4zJvou47RiObl/CIK+PdnbJB
NRxh6Dxa0HvfYg3BhNm0q2KBvanDraq53PZjtjMGgt7OzLClKA==
-----END RSA PRIVATE KEY-----"""

speed_levels = {
    'A': 30,
    'B': 31,
    'C': 32,
    'D': 33,
    'E': 34,
    'F': 35,
    'G': 36,
    'H': 37,
    'I': 38,
    'J': 39,
    'K': 40,
    'L': 41,
    'M': 42,
    'N': 43,
    'O': 44,
    'P': 45,
    'Q': 46,
    'R': 47,
    'S': 48,
    'T': 49,
    'U': 50,
    'V': 51,
    'W': 52,
    'X': 53,
    'Y': 54,
    'Z': 55,
    '0': 56,
    '1': 57,
    '2': 58,
    '3': 59,
    '4': 60,
    '5': 61,
    '6': 62,
    '7': 63,
    '8': 64,
    '9': 65,
    '-': 66,
    '=': 67,
    '[': 68,
    ']': 69,
    '(': 70,
    ')': 71,
    '@': 72,
    '#': 73,
    '$': 74,
    '%': 75,
    '^': 76,
    '&': 77,
    '*': 78,
    '_': 79,
    '+': 80,
    '{': 81,
    '}': 82,
    '|': 83,
    ';': 84,
    ':': 85,
    ',': 86,
    '.': 87,
    '/': 88,
    '<': 89,
    '>': 90,
    '?': 91,
    '`': 92,
    '~': 93,
    '!': 94,
    ' ': 0  # Space character with fan speed 0 (fan off)
}

def send_message(character):
    # Implement code to send the character to the receiver
    # This could involve using a wireless module (e.g., Wi-Fi, Bluetooth) or other communication protocols
    
    # Placeholder code to print the character for demonstration purposes
    print("Sending character:", character)

for character in private_key:
    if character in speed_levels:
        fan_speed = speed_levels[character]
        fan.ChangeDutyCycle(fan_speed)
        send_message(character)
        time.sleep(5)  # Adjust the delay as needed
    else:
        print("Invalid character:", character)

fan.stop()
IO.cleanup()
