# MQTT clients (laptop)

This folder covers the MQTT tests I ran from the laptop. Mosquitto was installed on the Raspberry Pi
and listening on port 1883.
I didn't keep standalone scripts: I used terminal commands (`mosquitto_sub` / `mosquitto_pub`).
They are collected here so the tests can be repeated without digging through the shell history.

## Lab settings (the ones I used)

- **Broker (Mosquitto):** `192.168.0.143`
- **Port:** `1883`
- **Main topics:**
  - `temperatura` (Pico with DS18B20)
  - `volt` (Pico with MCP3008)
- **Test / injection topic:**
  - `tf/sensor/analog`

## Subscribing (watching messages)

### Temperature

```bash
mosquitto_sub -h 192.168.0.143 -t 'temperatura' -v
```

### Voltage

```bash
mosquitto_sub -h 192.168.0.143 -t 'volt' -v
```
