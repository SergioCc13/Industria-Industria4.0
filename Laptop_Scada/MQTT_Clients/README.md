# MQTT clients (portátil)

Esta carpeta es para las pruebas MQTT que hice desde el portátil. En la Raspberry Pi se instaló Mosquitto y se levantó el servicio en 1883.
Yo no tenía scripts guardados como tal: lo que usé fueron comandos en terminal (`mosquitto_sub` / `mosquitto_pub`). 
Aquí lo dejo ordenado para poder repetirlo sin andar buscando en el historial.

## Datos del laboratorio (los que usé yo)

- **Broker (Mosquitto):** `192.168.0.143`
- **Puerto:** `1883`
- **Topics principales:**
  - `temperatura` (Pico DS18B20)
  - `volt` (Pico MCP3008)
- **Topic de pruebas/inyección:**
  - `tf/sensor/analog`

## Suscripción (ver mensajes)

### Temperatura
mosquitto_sub -h 192.168.0.143 -t 'temperatura' -v

### Voltaje
mosquitto_sub -h 192.168.0.143 -t 'volt' -v


