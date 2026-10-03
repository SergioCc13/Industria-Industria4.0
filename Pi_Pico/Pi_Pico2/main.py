import sys, ujson, time
from machine import Pin
import onewire, ds18x20
from umqtt.simple import MQTTClient
import network
from config import WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER, MQTT_USER, MQTT_PASS

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

while not wlan.isconnected():
    time.sleep(0.5)
print("Conexión Wi-Fi establecida:", wlan.ifconfig())

PIN = 16
ow = onewire.OneWire(Pin(PIN, Pin.IN, Pin.PULL_UP))
ds = ds18x20.DS18X20(ow)

BROKER = MQTT_BROKER
TOPIC = b"temperatura"

client = MQTTClient('pico2', BROKER, user=MQTT_USER, password=MQTT_PASS)

try:
    client.connect()
    print("Conectado al broker MQTT")
    mqtt_ok = True
except Exception as e:
    sys.stdout.write(ujson.dumps({"err": "mqtt_connect_fail", "error": str(e)}) + "\n")
    mqtt_ok = False

while True:
    roms = ds.scan()
    if not roms:
        sys.stdout.write(ujson.dumps({"err": "no_ds18b20"}) + "\n")
        time.sleep(1)
        continue

    try:
        ds.convert_temp()
        time.sleep_ms(750)
        t = ds.read_temp(roms[0])

        if t is None:
            sys.stdout.write(ujson.dumps({"err": "read_fail"}) + "\n")
        else:
            temp_redondeada = round(t, 1)
            payload = ujson.dumps({"payload_Temp": temp_redondeada})
            if mqtt_ok:
                client.publish(TOPIC, payload)
            sys.stdout.write(ujson.dumps({"t": temp_redondeada}) + "\n")
    except Exception as e:
        sys.stdout.write(ujson.dumps({"err": "read_fail", "error": str(e)}) + "\n")

    time.sleep(1)
