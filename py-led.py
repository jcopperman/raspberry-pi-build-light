import RPi.GPIO as GPIO
import json
from flask import Flask, request

app = Flask(__name__)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable GPIO warnings

# Define GPIO pin numbers
RED_LED_PIN = 17
GREEN_LED_PIN = 27
BLUE_LED_PIN = 18

# Set up GPIO pins as outputs
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

# Function to turn off all LEDs
def clear_leds():
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)

# Function to indicate workflow run conclusion
def indicate_workflow_conclusion(conclusion):
    clear_leds()
    if conclusion == 'success':
        GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    elif conclusion == 'failure':
        GPIO.output(RED_LED_PIN, GPIO.HIGH)
    elif conclusion == 'in_progress':
        GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(BLUE_LED_PIN, GPIO.HIGH)  # Default to blue for unknown status

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = json.loads(request.data)
        action = data.get('action')
        workflow_job = data.get('workflow_job', {})
        conclusion = workflow_job.get('conclusion', 'unknown')

        if action == 'completed' and conclusion is not None:
            indicate_workflow_conclusion(conclusion)
            return 'Success', 200
        else:
            return 'Action not supported', 400
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Blue LED indicates the workflow run is in progress
    GPIO.output(BLUE_LED_PIN, GPIO.HIGH)

    app.run(host='0.0.0.0', port=5000)
