import RPi.GPIO as IO
import time
import subprocess

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(14, IO.OUT)
fan = IO.PWM(14, 100)
fan.start(0)

minTemp = 25  # Minimum temperature threshold for anomaly detection
maxTemp = 80  # Maximum temperature threshold for anomaly detection
minSpeed = 0  # Minimum fan speed threshold for anomaly detection
maxSpeed = 100  # Maximum fan speed threshold for anomaly detection
anomaly_count = 0  # Counter to keep track of anomalies
interval = 2 * 60  # Interval in seconds (2 minutes)

def get_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not get temperature')

def renormalize(n, range1, range2):
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]

def detect_anomaly(temp, speed):
    if (temp < minTemp or temp > maxTemp) and (speed < minSpeed or speed > maxSpeed):
        return True
    return False

start_time = time.time()

while True:
    elapsed_time = time.time() - start_time

    if elapsed_time >= interval:
        start_time = time.time()
        anomaly_count = 0

    temp = get_temp()
    fan_speed = int(renormalize(temp, [minTemp, maxTemp], [minSpeed, maxSpeed]))
    fan.ChangeDutyCycle(fan_speed)

    if detect_anomaly(temp, fan_speed):
        anomaly_count += 1
        print(f"Detected anomaly in fan speed {anomaly_count} time(s) within the last 2 minutes.")

    time.sleep(5)
