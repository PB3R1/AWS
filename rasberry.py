import json
import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# AWS IoT Configuration
client = AWSIoTMQTTClient("raspberrypi")
client.configureEndpoint("d06831331ruuwf49ow23v-ats.iot.ap-south-1.amazonaws.com", 8883)
client.configureCredentials("/home/pi/certs/rootCA.pem", "/home/pi/certs/private.key", "/home/pi/certs/certificate.pem")

def update_wifi_config(client, userdata, message):
    payload = json.loads(message.payload)
    ssid = payload["ssid"]
    password = payload["password"]

    # Update wpa_supplicant.conf
    config = f'\nnetwork={{\n  ssid="{ssid}"\n  psk="{password}"\n}}\n'
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as f:
        f.write(config)
    
    # Restart networking
    os.system("sudo wpa_cli -i wlan0 reconfigure")

client.connect()
client.subscribe("pi/wifi-config", 1, update_wifi_config)

while True:
    pass