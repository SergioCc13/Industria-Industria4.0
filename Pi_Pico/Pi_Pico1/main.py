import sys, ujson, time
from machine import Pin, SPI
from mcp3008 import MCP3008
from umqtt.simple import MQTTClient
import network

ssid = 'Vodafone-2F5B'
password = 'Lacanonja'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(0.5)
print("Conexión Wi-Fi establecida:", wlan.ifconfig())

broker = '192.168.0.143'
MQTT_USER = 'sensor1'
MQTT_PASS = '1999'

client = MQTTClient('pico1', broker, user=MQTT_USER, password=MQTT_PASS)

try:
    client.connect()
    print("Conectado al broker MQTT")
    mqtt_ok = True
except Exception as e:
    sys.stdout.write(ujson.dumps({"err": "mqtt_connect_fail", "error": str(e)}) + "\n")
    mqtt_ok = False

spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5, Pin.OUT, value=1)
adc = MCP3008(spi, cs, vref=3.3)

while True:
    ch0 = adc.read_raw(0)
    payload = {"ts": time.time(), "ch0_raw": ch0}
    if mqtt_ok:
        client.publish(b"volt", ujson.dumps(payload))
    print(ujson.dumps(payload))
    time.sleep(1)
